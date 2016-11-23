import logging
import math
import os
import re
import time
from typing import List

import requests
import vk.exceptions
from vk_app import App
from vk_app.attachables import VKPhoto, VKPhotoAlbum, VKVideo
from vk_app.post import VKPost
from vk_app.utils import make_delayed, show_captcha

from vk_scheduler.settings import (CONFIGURATION_FILE_PATH, TMP_DRC_ABSPATH, CAPTCHA_IMG_ABSPATH,
                                   LINKS_SEP, LINKS_BLOCK_RE, IMG_LINK_RE, EXTERNAL_VIDEO_LINK_RE,
                                   MINIMAL_INTERVAL_BETWEEN_POST_EDITING_REQUESTS_IN_SECONDS, config)
from vk_scheduler.utils import get_vk_object_ids, download, clear_drc, get_vk_object_links


class Scheduler(App):
    def __init__(self, app_id: int = 0, group_id: int = 1, user_login: str = '', user_password: str = '',
                 scope: str = '', access_token: str = '', api_version: str = '5.57',
                 last_check_utc_timestamp: int = 0):
        super().__init__(app_id, user_login, user_password, scope, access_token, api_version)
        self.group_id = group_id
        self.last_check_utc_timestamp = last_check_utc_timestamp

    def check_posts(self):
        for ind, unchecked_post in enumerate(self.unchecked_posts_by_community):
            logging.info('Processing post: https://vk.com/wall{}'.format(unchecked_post.vk_id))
            try:
                self.edit_post(unchecked_post)
            except vk.exceptions.VkAPIError:
                logging.exception('Some error arose. Post will not be edited. Continue...')
            logging.info('Number of posts edited so far {}'.format(ind + 1))
        self.last_check_utc_timestamp = int(time.time())
        self.log_last_check_utc_timestamp()
        clear_drc(TMP_DRC_ABSPATH)

    def edit_post(self, post: VKPost):
        search_res = re.search(LINKS_BLOCK_RE, post.text)
        if search_res is None:
            return
        links_block = search_res.group().strip()
        links = list(link.strip() for link in links_block.split(LINKS_SEP))

        photos_links = get_vk_object_links(VKPhoto, links)
        photo_albums_links = get_vk_object_links(VKPhotoAlbum, links)
        videos_links = get_vk_object_links(VKVideo, links)
        images_links = list(
            link
            for link in links
            if re.match(IMG_LINK_RE, link) is not None
        )
        external_videos_links = list(
            link
            for link in links
            if re.match(EXTERNAL_VIDEO_LINK_RE, link) is not None
        )

        if photos_links:
            photos_by_links = self.get_photos_by_links(photos_links)
        if photo_albums_links:
            photo_albums = self.get_photo_albums_by_links(photo_albums_links)
        if images_links:
            photos_by_images_links = self.get_photos_by_images_links(images_links)

        if videos_links:
            videos_by_links = self.get_videos_by_links(videos_links)
        if external_videos_links:
            videos_by_external_links = self.get_videos_by_external_links(external_videos_links)

        attachment_id_format = '{key}{vk_id}'
        attachments_ids = list(
            attachment_id_format.format(key=key, vk_id=vk_attachment.vk_id)
            for attachment in post.attachments
            for key, vk_attachment in attachment.items()
        )
        obscure_links = list()
        for link in links:
            if len(attachments_ids) >= 10:
                logging.error('Too many attachments, next link would be ignored: {}'.format(link))
                obscure_links.append(link)
                continue
            attachment = None

            if link in photos_links:
                attachment = next((photo for photo in photos_by_links if photo.vk_id in link), None)
            elif link in photo_albums_links:
                attachment = next((photo_album for photo_album in photo_albums if photo_album.vk_id in link), None)
            elif link in images_links:
                attachment = photos_by_images_links.pop(0) if photos_by_images_links else None
            elif link in videos_links:
                attachment = next((video for video in videos_by_links if video.vk_id in link), None)
            elif link in external_videos_links:
                attachment = next((video for video in videos_by_external_links if video.player_link in link), None)

            if attachment is not None:
                attachments_ids.append(
                    attachment_id_format.format(key=attachment.key(), vk_id=attachment.vk_id)
                )
            else:
                logging.error('Unknown link type: {}'.format(link))
                obscure_links.append(link)

        attachments = ','.join(attachments_ids)
        message = post.text.replace(links_block, LINKS_SEP.join(obscure_links))
        self.post_edited(post, message, attachments)

    @make_delayed(MINIMAL_INTERVAL_BETWEEN_POST_EDITING_REQUESTS_IN_SECONDS)
    def post_edited(self, post: VKPost, message: str, attachments: str, **params):
        while True:
            try:
                self.api_session.wall.edit(owner_id=post.owner_id, post_id=post.object_id,
                                           message=message, attachments=attachments, **params)
                return
            except vk.exceptions.VkAPIError as error:
                logging.exception('')
                if error.code == error.CAPTCHA_NEEDED:
                    download(error.captcha_img, CAPTCHA_IMG_ABSPATH)
                    show_captcha(CAPTCHA_IMG_ABSPATH)
                    captcha_key = input('Please enter the captcha key from image:\n')
                    os.remove(CAPTCHA_IMG_ABSPATH)
                    params['captcha_sid'] = error.captcha_sid
                    params['captcha_key'] = captcha_key
                else:
                    return

    @property
    def unchecked_posts_by_community(self) -> List[VKPost]:
        params = dict(
            owner_id=-self.group_id,
            offset=0,
            count=50,
            filter='owner'
        )
        response = self.api_session.wall.get(**params)
        raw_posts = response['items']
        total_count = response['count']
        while raw_posts[-1]['date'] > self.last_check_utc_timestamp and params['offset'] < total_count:
            params['offset'] += params['count']
            response = self.api_session.wall.get(**params)
            raw_posts.extend(response['items'])
        raw_posts.sort(key=lambda post: post.date_time)
        for raw_post in raw_posts:
            if raw_post['date'] > self.last_check_utc_timestamp:
                yield VKPost.from_raw(raw_post)

    def get_photos_by_links(self, photos_links: List[str]) -> List[VKPhoto]:
        photos_ids = get_vk_object_ids(VKPhoto, photos_links)
        raw_photos = self.api_session.photos.getById(photos=','.join(photos_ids))
        photos = list(VKPhoto.from_raw(raw_photo) for raw_photo in raw_photos)
        return photos

    def get_videos_by_links(self, videos_links: List[str]) -> List[VKVideo]:
        videos_ids = get_vk_object_ids(VKVideo, videos_links)
        raw_videos = self.api_session.video.get(videos=','.join(videos_ids))['items']
        videos = list(VKVideo.from_raw(raw_photo) for raw_photo in raw_videos)
        return videos

    def get_photo_albums_by_links(self, albums_links: List[str]) -> List[VKVideo]:
        albums_ids = get_vk_object_ids(VKPhotoAlbum, albums_links)
        owners_ids_albums_ids = dict()
        for album_id in albums_ids:
            album_owner_id, album_object_id = album_id.split('_')
            owners_ids_albums_ids.setdefault(album_owner_id, []).append(album_object_id)
        raw_albums = list()
        for owner_id, albums_ids in owners_ids_albums_ids.items():
            raw_albums.extend(
                self.api_session.photos.getAlbums(owner_id=owner_id, album_ids=','.join(albums_ids))['items']
            )
        albums = list(VKPhotoAlbum.from_raw(raw_album) for raw_album in raw_albums)
        return albums

    def get_photos_by_images_links(self, images_links: List[str]) -> List[VKPhoto]:
        photos = list()
        method = VKPhoto.identify_save_method('wall')
        for i in range(math.ceil(len(images_links) / 7)):

            upload_url = self.get_upload_server_url(VKPhoto.identify_getUploadServer_method('wall'),
                                                    group_id=self.group_id)
            images = list()
            for ind, image_link in enumerate(images_links[i * 7: min((i + 1) * 7, len(images_links))]):
                image_name = image_link.split('/')[-1]
                save_path = os.path.join(TMP_DRC_ABSPATH, image_name)
                download(image_link, save_path)
                with open(save_path, mode='rb') as file:
                    images.append(
                        (
                            'file',
                            (image_name, file.read())
                        )
                    )
            for image in images:
                raw_photo, = self.upload_files_on_vk_server(method=method, upload_url=upload_url,
                                                            files=[image], group_id=self.group_id)
                photos.append(VKPhoto.from_raw(raw_photo))
        return photos

    def get_videos_by_external_links(self, video_links: List[str]) -> List[VKVideo]:
        video_ids = list(
            '{owner_id}_{video_id}'.format(**response)
            for response in self.videos_by_external_links(video_links)
        )
        raw_videos = self.api_session.video.get(videos=','.join(video_ids))['items']
        videos = list(VKVideo.from_raw(raw_video) for raw_video in raw_videos)
        return videos

    def videos_by_external_links(self, links: List[str]):
        for link in links:
            response = self.api_session.video.save(link=link, group_id=self.group_id)
            with requests.Session() as session:
                session.post(response['upload_url'])
            yield response

    def log_last_check_utc_timestamp(self):
        config.set('schedule', 'last_check_utc_timestamp', value=str(self.last_check_utc_timestamp))
        with open(CONFIGURATION_FILE_PATH, mode='w') as configuration_file:
            config.write(configuration_file)

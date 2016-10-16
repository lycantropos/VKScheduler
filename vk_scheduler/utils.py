import os
import re
import shutil
from typing import List

from PIL import Image
from vk_app.services.loading import download
from vk_app.utils import make_delayed

from vk_scheduler.settings import MINIMAL_INTERVAL_BETWEEN_DOWNLOAD_REQUESTS_IN_SECONDS, VK_OBJECTS_LINK_RES

download = make_delayed(MINIMAL_INTERVAL_BETWEEN_DOWNLOAD_REQUESTS_IN_SECONDS)(download)


def get_vk_object_ids(cls: type, links: List[str]) -> List[str]:
    return list(
        re.match(VK_OBJECTS_LINK_RES[cls], link).group(1)
        for link in links
    )


def get_vk_object_links(cls: type, links: List[str]) -> List[str]:
    return list(
        link
        for link in links
        if re.match(VK_OBJECTS_LINK_RES[cls], link) is not None
    )


def filter_by_re(regexp: str, *strings):
    return list(
        string
        for string in strings
        if re.match(regexp, string) is not None
    )


def show_captcha(path: str):
    with Image.open(path) as img:
        size = img.size
        size = size[0] * 4, size[1] * 4
        img = img.resize(size)
        img.show(path)


def clear_drc(path: str):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

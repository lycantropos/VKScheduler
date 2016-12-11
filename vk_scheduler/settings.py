import configparser
import os
import re

from vk_app.attachables import VKAttachable
from vk_app.utils import get_all_subclasses

CONFIGURATION_FILE_NAME = 'configuration.conf'
CURRENT_FILE_PATH = os.path.realpath(__file__)
CURRENT_FILE_ABSPATH = os.path.abspath(CURRENT_FILE_PATH)
BASE_DIR = os.path.dirname(CURRENT_FILE_ABSPATH)
CONFIGURATION_FILE_FOLDER = 'configurations'
CONFIGURATION_FILE_PATH = os.path.join(BASE_DIR, CONFIGURATION_FILE_FOLDER, CONFIGURATION_FILE_NAME)
config = configparser.ConfigParser()
config.read(CONFIGURATION_FILE_PATH)

user = config['user']
USER_LOGIN = user.get('user_login')
USER_PASSWORD = user.get('user_password')
ACCESS_TOKEN = user.get('access_token')

app = config['app']
APP_ID = int(app.get('app_id'))
SCOPE = app.get('scope')
GROUP_ID = int(app.get('group_id'))

schedule = config['schedule']
CHECKING_INTERVAL_IN_SECONDS = int(schedule.get('checking_interval_in_seconds'))
LAST_CHECK_UTC_TIMESTAMP = int(schedule.get('last_check_utc_timestamp'))

files = config['files']
TMP_DRC_ABSPATH = files.get('tmp_drc_abspath')
VIDEO_SERVICES = list(
    re.sub(r'^w{3}\.(?=.+$)', '', video_service.strip())
    for video_service in files.get('video_services').split(',')
)

logger = config['logger']
LOGS_PATH = logger.get('logs_path')
LOGGING_CONFIG_PATH = logger.get('logging_config_path')

CAPTCHA_IMG_ABSPATH = os.path.join(TMP_DRC_ABSPATH, 'captcha.png')

MINIMAL_INTERVAL_BETWEEN_DOWNLOAD_REQUESTS_IN_SECONDS = 0.35
MINIMAL_INTERVAL_BETWEEN_POST_EDITING_REQUESTS_IN_SECONDS = 25

MORE_INFO_BLOCK_RE = r'(?:\n\nПодробности:.*)?$'
LINKS_SEP = '\n'
LINKS_BLOCK_RE = re.compile(
    r'\n(?:(?:https?:\/\/(?:.+?)(?:\/.*)){sep})*(?:https?:\/\/(?:.+?)(?:\/.*))'.format(sep=LINKS_SEP) + \
    r'(?={})'.format(MORE_INFO_BLOCK_RE))

IMG_LINK_RE = re.compile(r'^https?:\/\/(?:.+?)(?:\/.*\.jpg)$')
EXTERNAL_VIDEO_LINK_RE = re.compile(''.join([
    r'^https?:\/\/(?:',
    '|'.join(
        '(?:(?:www\.)?{video_service})'.format(video_service=video_service.replace('.', '\.'))
        for video_service in VIDEO_SERVICES
    ),
    ')(?:\/.*)$']))

VK_ID_RE = r'(-?\d+_\d+)'
VK_OBJECT_LINK_RE_PATTERN = r'^https?:\/\/(?:www|m\.)?vk\.com\/.*(?:{vk_object_id_re}).*$'
VK_OBJECTS_LINK_RES = {
    cls: re.compile(VK_OBJECT_LINK_RE_PATTERN
                    .format(vk_object_id_re=cls.key() + VK_ID_RE))
    for cls in get_all_subclasses(VKAttachable)
    if cls.key()
    }

import logging
import os
import time

import click
from vk_app.services.logging_config import LoggingConfig
from vk_app.utils import make_periodic

from vk_scheduler.app import VKScheduler
from vk_scheduler.settings import (TMP_DRC_ABSPATH, APP_ID, USER_LOGIN, USER_PASSWORD, SCOPE, GROUP_ID, BASE_DIR,
                                   LOGGING_CONFIG_PATH, LOGS_PATH, LAST_CHECK_UTC_TIMESTAMP,
                                   CHECKING_INTERVAL_IN_SECONDS)


@click.group("run", invoke_without_command=False)
def run():
    pass


@run.command("edit_bot")
def edit_bot():
    """Edits new (unchecked) posts periodically"""
    if not os.path.exists(TMP_DRC_ABSPATH):
        os.mkdir(TMP_DRC_ABSPATH)

    LoggingConfig(BASE_DIR, LOGGING_CONFIG_PATH, LOGS_PATH).set()
    vk_scheduler = VKScheduler(app_id=APP_ID, group_id=GROUP_ID, user_login=USER_LOGIN, user_password=USER_PASSWORD,
                               scope=SCOPE, last_check_utc_timestamp=LAST_CHECK_UTC_TIMESTAMP)

    sec_since_last_call = time.time() - vk_scheduler.last_check_utc_timestamp
    wait_sec = CHECKING_INTERVAL_IN_SECONDS - sec_since_last_call
    if wait_sec > 0.:
        logging.info(
            "Last call of `{}` was performed {:.2f} seconds ago, next call will be after {:.2f} seconds".format(
                VKScheduler.check_posts.__name__, sec_since_last_call, wait_sec
            )
        )
        time.sleep(wait_sec)

    vk_scheduler.check_posts = make_periodic(CHECKING_INTERVAL_IN_SECONDS)(vk_scheduler.check_posts)
    vk_scheduler.check_posts()


if __name__ == '__main__':
    run()

import logging
import os
import time

import click
from vk_app.services.logging_config import set_logging_config
from vk_app.utils import make_periodic, check_dir

from vk_scheduler.app import Scheduler
from vk_scheduler.settings import (TMP_DRC_ABSPATH, APP_ID, USER_LOGIN, USER_PASSWORD, SCOPE, GROUP_ID, BASE_DIR,
                                   LOGGING_CONFIG_PATH, LOGS_PATH, LAST_CHECK_UTC_TIMESTAMP,
                                   CHECKING_INTERVAL_IN_SECONDS)


@click.group('run', invoke_without_command=False)
def run():
    pass


@run.command('edit_bot')
def edit_bot():
    """Edits new (unchecked) posts periodically"""
    check_dir(TMP_DRC_ABSPATH, create=True)

    scheduler = Scheduler(app_id=APP_ID, group_id=GROUP_ID, user_login=USER_LOGIN, user_password=USER_PASSWORD,
                          scope=SCOPE, last_check_utc_timestamp=LAST_CHECK_UTC_TIMESTAMP)

    sec_since_last_call = time.time() - scheduler.last_check_utc_timestamp
    wait_sec = CHECKING_INTERVAL_IN_SECONDS - sec_since_last_call
    if wait_sec > 0.:
        logging.info(
            'Last call of `{}` was performed {:.2f} seconds ago, next call will be after {:.2f} seconds'.format(
                Scheduler.check_posts.__name__, sec_since_last_call, wait_sec
            )
        )
        time.sleep(wait_sec)

    scheduler.check_posts = make_periodic(CHECKING_INTERVAL_IN_SECONDS)(scheduler.check_posts)
    scheduler.check_posts()


if __name__ == '__main__':
    set_logging_config(BASE_DIR, LOGGING_CONFIG_PATH, LOGS_PATH)
    run()

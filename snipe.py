import time

import datetime as datetime
from dateutil.relativedelta import relativedelta

from util import logs_manager as log
import sys
import util.utils as util
from util.classes.config import Config
import util.naming_system as name

if __name__ == "__main__":
    log.on_load()
    log.info("Loading accounts from file.")

    accounts = util.get_accounts()
    if len(accounts) == 0:
        log.error("No accounts were loaded from file. Please check accounts.txt and try again.")
        sys.exit(0)

    log.info(f"{len(accounts)} account(s) have been loaded from file.")

    config = Config()
    log.info("Loaded config")

    username = log.custom_input("What name do you want to snipe?: ")
    droptime = None  # droptime = epoch

    naming_system = config.get("timing_system")
    if naming_system == "namemc":
        droptime = name.namemc(username)

    if droptime is None:
        log.error("Failed to get droptime.")
        sys.exit(0)

    login_time = droptime - int(config.get("auth_delay"))
    login_time_datetime = datetime.datetime.fromtimestamp(login_time)
    rd = relativedelta(datetime.datetime.now(), login_time_datetime)
    log.info(
        f"Logging in at {login_time_datetime}. ({-rd.hours} hour(s), {-rd.minutes} minute(s) and {-rd.seconds} second(s))")

    while datetime.datetime.now().timestamp() < login_time:
        time.sleep(1)

    # start login

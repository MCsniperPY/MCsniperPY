import typer
import logging
import datetime
import sys
import time

from dateutil.relativedelta import relativedelta
from util import logs_manager as log
from util import utils as util
from util.classes.config import Config
from util import naming_system as name


def main(username: str, delay: int, debug: bool = False):
    if debug:
        logging.basicConfig(format=log.debug("%(message)s"), level=logging.DEBUG)

    log.on_load()
    log.info("Loading accounts from file.")

    accounts = util.get_accounts()
    if len(accounts) == 0:
        log.error("No accounts were loaded from file. Please check accounts.txt and try again.")
        sys.exit(0)

    log.info(f"{len(accounts)} account(s) have been loaded from file.")

    config = Config()
    log.info("Loaded config")

    log.info(f"Sniping username: {username}")
    log.info(f"Delay (ms): {delay}")

    droptime = None  # droptime = epoch

    naming_system = config.get("timing_system")
    if naming_system == "namemc":
        droptime = name.namemc(username)

    if droptime is None:
        log.error("Failed to get droptime.")
        sys.exit(0)

    auth_delay = int(config.get("auth_delay"))
    drop_time_datetime = datetime.datetime.fromtimestamp(droptime)
    rd = relativedelta(datetime.datetime.now(), drop_time_datetime)

    for acc in accounts:
        acc.authenticate()
        time.sleep(auth_delay / 1000)

    log.info(
        f"Sniping at {drop_time_datetime}. ({-rd.hours} hour(s), {-rd.minutes} minute(s) and {-rd.seconds} second(s))")

    while datetime.datetime.now().timestamp() < droptime:
        time.sleep(1)


if __name__ == "__main__":
    typer.run(main)

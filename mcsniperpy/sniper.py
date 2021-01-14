import aiohttp

from .util import request_manager
from .util import utils as util


class Sniper:
    def __init__(self,
                 colorer,
                 logger):
        self.color = colorer
        self.logger = logger
        self.session = request_manager.RequestManager(
            aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(limit=300),
                headers={}
            )
        )

    def run(self):
        color = self.color
        log = self.logger

        log.info(f"{color.white}Hey, {color.red}hii.")

        log.info("Loading accounts from file.")

        accounts = util.get_accounts()
        if len(accounts) == 0:
            log.error("No accounts were loaded from file. Please check accounts.txt and try again.")
            sys.exit(0)

        log.info(f"{len(accounts)} account(s) have been loaded from file.")

        config = Config()
        log.debug("Loaded config")

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

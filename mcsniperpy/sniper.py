import asyncio

import aiohttp

from .util import request_manager
from .util import utils as util
from .util.classes.config import BackConfig


class Sniper:
    def __init__(self,
                 colorer,
                 logger):
        self.color = colorer
        self.log = logger
        self.session = request_manager.RequestManager(
            aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(limit=300),
                headers={}
            )
        )

        self.target = str()  # target username
        self.offset = int()  # Time offset (e.g., 400 = snipe the name 400ms early)

        self.back_config = None  # util.classes.config.BackConfig

        self.data = None

    @property
    def initialized(self):
        return self.config.init_path != ""

    def init(self):
        if self.initilized:
            self.log.debug("Already initialized")
        else:
            self.log.debug("Not initialized")

    def run(self, target=None, offset=None):

        if target is None:
            self.target = self.log.input("Target Username:")

        if offset is None:
            self.offset = self.log.input("Time Offset:")

        self.log.info(f"{self.color.white}Hey, {self.color.red}hii.")

        self.config = BackConfig()
        self.log.debug("loaded config")

        self.log.debug("Loading accounts from file.")

        accounts = util.get_accounts()
        if len(accounts) == 0:
            self.log.error("No accounts were loaded from file. Please check accounts.txt and try again.")
            sys.exit(0)

        self.log.info(f"{len(accounts)} account(s) have been loaded from file.")

        self.log.info(f"Sniping username: {username}")
        self.log.info(f"Delay (ms): {delay}")

        droptime = name.namemc(username)

        if droptime is None:
            self.log.error("Failed to get droptime.")
            sys.exit(0)

        auth_delay = int(config.get("auth_delay"))
        drop_time_datetime = datetime.datetime.fromtimestamp(droptime)
        rd = relativedelta(datetime.datetime.now(), drop_time_datetime)

        for acc in accounts:
            acc.authenticate()
            time.sleep(auth_delay / 1000)

        while datetime.datetime.now().timestamp() < droptime:
            time.sleep(1)

        self.on_shutdown()

    def on_shutdown(self):
        asyncio.get_event_loop().run_until_complete(self.session.session.close())

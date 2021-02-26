import asyncio
import datetime
import os.path
from datetime import datetime

import aiohttp
from dateutil import relativedelta

from .util import request_manager
from .util import utils as util
from .util.classes.config import BackConfig, populate_configs, Config
from .util.name_system import api_timing


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

        self.config = None  # util.classes.config.BackConfig
        self.user_config = None  # util.classes.config.Config

        self.data = None

        self.accounts = []  # list of Accounts

    @property
    def initialized(self):
        return self.config.init_path != ""

    def init(self):

        populate_configs()

    async def run(self, target=None, offset=None):

        self.config = BackConfig()
        self.log.debug(f"Using sniping path of {self.config.init_path}")

        self.user_config = Config(os.path.join(self.config.init_path, 'config.ini'))

        if target is None:
            self.log.debug('No username detected')
            self.target = self.log.input("Target Username:")
        else:
            self.log.info(f"Sniping username: {target}")

        if offset is None:
            self.log.debug('no offset detected')
            self.offset = self.log.input("Time Offset:")
        else:
            self.log.info(f"Offset (ms): {offset}")

        self.accounts = util.parse_accs(os.path.join(self.config.init_path, "accounts.txt"))

        if len(self.accounts) == 0:
            self.log.info(f"{len(self.accounts)} account has been loaded from file.")
        else:
            self.log.info(f"{len(self.accounts)} accounts have been loaded from file.")

        droptime = await api_timing(target, self.session)

        if droptime is None:
            self.log.error("Failed to get droptime.")
            sys.exit(0)

        auth_delay = self.user_config.config['accounts'].getint('authentication_delay')
        drop_time_datetime = datetime.fromtimestamp(droptime)
        rd = relativedelta.relativedelta(datetime.now(), drop_time_datetime)

        await asyncio.gather(*[acc.fully_authenticate(session=self.session) for acc in self.accounts])

        while datetime.now().timestamp() < droptime:
            await asyncio.sleep(.01)

        await asyncio.gather(*[acc.snipe(target) for acc in self.accounts])

        self.on_shutdown()

    def on_shutdown(self):
        asyncio.get_event_loop().run_until_complete(self.session.session.close())

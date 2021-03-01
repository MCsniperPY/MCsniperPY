import asyncio
import datetime
import os.path
import time
from datetime import datetime

import aiohttp

from .util import request_manager
from .util import utils as util
from .util.classes.config import BackConfig, populate_configs, Config
from .util.name_system import api_timing, namemc_timing


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
            target = self.log.input("Target Username:")
        else:
            self.log.info(f"Sniping username: {target}")

        if offset is None:
            self.log.debug('no offset detected')
            offset = self.log.input("Time Offset:")
        else:
            self.log.info(f"Offset (ms): {offset}")

        self.accounts = util.parse_accs(os.path.join(self.config.init_path, "accounts.txt"))

        timing_system = self.user_config.config['sniper'].get('timing_system', 'kqzz_api').lower()
        if timing_system == 'kqzz_api':
            droptime = await api_timing(target, self.session)
        elif timing_system == 'namemc':
            droptime = await namemc_timing(target, self.session)
        else:
            droptime = await api_timing(target, self.session)


        start_auth = self.user_config.config['accounts'].getint('start_authentication', '720')

        time_until_authentication = 0 if time.time() > (droptime - start_auth) else droptime - start_auth

        await asyncio.sleep(time_until_authentication)
        await asyncio.gather(*[acc.fully_authenticate(session=self.session) for acc in self.accounts])

        while datetime.now().timestamp() < droptime:
            await asyncio.sleep(.001)

        await asyncio.gather(*[acc.snipe(target) for _ in range(3) for acc in self.accounts])

    def on_shutdown(self):
        asyncio.run(self.session.session.close())

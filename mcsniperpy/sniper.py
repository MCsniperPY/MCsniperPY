import asyncio
import os.path
import time

import aiohttp

from mcsniperpy.util import request_manager
from mcsniperpy.util import utils as util
from mcsniperpy.util.classes.config import BackConfig, populate_configs, Config
from mcsniperpy.util.name_system import api_timing, namemc_timing


class Sniper:
    def __init__(self,
                 colorer,
                 logger):
        self.color = colorer
        self.log = logger
        self.session = request_manager.RequestManager(
            None  # aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=300),headers={})
        )

        self.target = str()  # target username
        self.offset = int()  # Time offset (e.g., 400 = snipe the name 400ms early)

        self.config = None  # util.classes.config.BackConfig
        self.user_config = None  # util.classes.config.Config

        self.data = None

        self.accounts = []  # list of Accounts

    @property
    def initialized(self):
        return self.config.config['sniper'].get('init_path', '') != ''

    @staticmethod
    def init() -> None:

        populate_configs()

    async def run(self, target=None, offset=None):

        self.session.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=300),
            headers={}
        )

        self.config = BackConfig()
        self.log.debug(f"Using sniping path of {self.config.config['sniper'].get('init_path')}")

        self.user_config = Config(os.path.join(self.config.config['sniper'].get('init_path'), 'config.ini'))

        if target is None:
            self.log.debug('No username detected')
            target = self.log.input("Target Username:")
            if target is None:
                self.log.error(f'invalid input "{target}".')
        else:
            self.log.info(f"Sniping username: {target}")

        if offset is None:
            self.log.debug('no offset detected')
            offset = self.log.input("Time Offset:")
            if offset is None or not util.is_float(offset):
                self.log.error(f'Invalid offset input: "{offset}"')
                util.close(1)
            else:
                offset = float(offset)
        else:
            self.log.info(f"Offset (ms): {offset}")

        self.accounts = util.parse_accs(os.path.join(self.config.config['sniper'].get('init_path'), "accounts.txt"))

        timing_system = self.user_config.config['sniper'].get('timing_system', 'kqzz_api').lower()
        start_auth = self.user_config.config['accounts'].getint('start_authentication', '720')

        if timing_system == 'kqzz_api':
            droptime = await api_timing(target, self.session)
        elif timing_system == 'namemc':
            droptime = await namemc_timing(target, self.session)
        else:
            droptime = await api_timing(target, self.session)

        req_count = self.user_config.config['sniper'].getint('snipe_requests', '3')

        await self.snipe(droptime, target, offset, req_count, start_auth)

    async def snipe(self, droptime, target, offset, req_count, start_auth):

        authentication_coroutines = [acc.fully_authenticate(session=self.session) for acc in self.accounts]
        pre_snipe_coroutines = [acc.snipe_connect() for _ in range(req_count) for acc in self.accounts]  # For later use

        time_until_authentication = 0 if time.time() > (droptime - start_auth) else (droptime - start_auth) - time.time()

        self.log.debug(f'authorizing accounts in {time_until_authentication} seconds.')

        await asyncio.sleep(time_until_authentication)

        await asyncio.gather(*authentication_coroutines)

        for acc in self.accounts:
            acc.encode_snipe_data(target)

        time_until_connect = 0 if time.time() > (droptime - 20) else (droptime - 20) - time.time()

        self.log.debug(f'Connecting in {time_until_connect} seconds.')

        await asyncio.sleep(time_until_connect)

        await asyncio.gather(*pre_snipe_coroutines)

        snipe_coroutines = [acc.snipe(acc.readers_writers[i][1]) for i in range(req_count) for acc in self.accounts]

        while time.time() < droptime - offset / 1000:
            await asyncio.sleep(0.00001)  # bad timing solution

        await asyncio.gather(*snipe_coroutines)  # Sends the snipe requests
        responses = await asyncio.gather(
            *[acc.snipe_read(target, acc.readers_writers[i][0], acc.readers_writers[i][1]
                             ) for i in range(req_count) for acc in self.accounts]
        )  # Reads the responses

        for is_success, email in responses:
            if is_success:
                success_acc = util.find_acc_by_email(email, self.accounts)
                self.log.info(f'{self.color.white}[{self.color.l_green}success{self.color.white}]{self.color.reset} '
                              f'sniped {self.target} onto {success_acc.email}')

    def on_shutdown(self):
        if self.session.session is not None:
            asyncio.run(self.session.session.close())
        if self.log is not None:
            self.log.shutdown()

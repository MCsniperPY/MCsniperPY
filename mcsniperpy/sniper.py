import asyncio
import os.path
import time
from typing import List

import aiohttp

from mcsniperpy.util import announce, request_manager
from mcsniperpy.util import utils as util
from mcsniperpy.util.classes.config import BackConfig, Config, populate_configs
from mcsniperpy.util.name_system import api_timing, namemc_timing, teun_timing, coolkidmacho_timing


class Sniper:
    def __init__(self, colorer, logger):
        self.color = colorer
        self.log = logger
        self.session = request_manager.RequestManager(
            # aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=300),headers={})
            None
        )

        self.target = str()  # target username
        self.offset = int()  # Time offset (e.g., 400 = snipe the name 400ms early)

        self.config = None  # util.classes.config.BackConfig
        self.user_config = None  # util.classes.config.Config

        self.data = None

        self.accounts = []  # list of Accounts

        # sniper

        self.timing_system = "kqzz_api"
        self.auto_claim_namemc = False
        self.snipe_requests = 3

        # accounts

        self.max_accounts = 1
        self.authentication_delay = 500
        self.start_authentication = 720 * 60

        # skin

        self.change_skin_on_snipe = False
        self.skin_change_type = "url"
        self.skin = ""
        self.skin_variant = "classic"

        # announce
        self.do_announce = False
        self.announce_code = ""
        self.webhook_urls = List[str]
        self.webhook_format = ""

    @property
    def initialized(self):
        return self.config.config["sniper"].get("init_path", "") != ""

    @staticmethod
    def init(no_confirm=False) -> None:
        populate_configs(no_confirm)

    def get_config_values(self):
        # sniper

        self.timing_system = (
            self.user_config.config["sniper"].get(
                "timing_system", "kqzz_api").lower()
        )
        self.auto_claim_namemc = self.user_config.config["sniper"].getboolean(
            "auto_claim_namemc", "no"
        )
        self.snipe_requests = self.user_config.config["sniper"].getint(
            "snipe_requests", "3"
        )

        # accounts

        self.max_accounts = self.user_config.config["accounts"].getint(
            "max_accounts", "1"
        )
        self.authentication_delay = self.user_config.config["accounts"].getint(
            "authentication_delay", "500"
        )
        self.start_authentication = self.user_config.config["accounts"].getint(
            "start_authentication", "720"
        ) * 60

        # skin

        self.change_skin_on_snipe = self.user_config.config["skin"].getboolean(
            "change_skin_on_snipe", "no"
        )
        self.skin_change_type = self.user_config.config["skin"].get(
            "skin_change_type", "url"
        )
        self.skin = self.user_config.config["skin"].get("skin", "")
        self.skin_variant = self.user_config.config["skin"].get(
            "skin_variant", "classic"
        )

        if self.skin_change_type == "file":
            with open(
                os.path.join(
                    self.config.config["sniper"].get(
                        "init_path", ""
                    ),
                    self.skin
                ),
                "rb"
            ) as f:
                self.skin = f.read

        # announce
        self.do_announce = self.user_config.config["announce"].getboolean(
            "announce_snipe", "no"
        )
        self.announce_code = self.user_config.config["announce"].get(
            "announce_code", ""
        )
        webhook_urls = self.user_config.config["announce"].get(
            "webhook_urls", "")
        self.webhook_urls = webhook_urls.split(",")
        self.webhook_format = self.user_config.config["announce"].get(
            "webhook_format", "sniped `{name}` with `{searches}` searches!"
        )

    async def run(self, target=None, offset=None):

        self.session.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=300), headers={}
        )

        self.config = BackConfig()
        self.log.debug(
            "Using sniping path of"
            f" {self.config.config['sniper'].get('init_path')}"
        )

        self.user_config = Config(
            os.path.join(self.config.config["sniper"].get(
                "init_path"), "config.ini")
        )

        self.get_config_values()

        if target is None:
            self.log.debug("No username detected")
            target = self.log.input("Target Username:")
            if target is None:
                self.log.error(f'invalid input "{target}".')
        else:
            self.log.info(f"Sniping username: {target}")

        if offset is None:
            self.log.debug("no offset detected")
            offset = self.log.input("Time Offset:")
            if offset is None or not util.is_float(offset):
                self.log.error(f'Invalid offset input: "{offset}"')
                util.close(1)
            else:
                offset = float(offset)
        else:
            self.log.info(f"Offset (ms): {offset}")

        self.accounts = util.parse_accs(
            os.path.join(self.config.config["sniper"].get(
                "init_path"), "accounts.txt")
        )
        if len(self.accounts) > self.max_accounts:
            self.log.warn("Using more than 1 account is entirely innefective!")
            self.log.warn("For the best chances use only 1 account.")

        droptime = await {
            "kqzz_api": api_timing,
            "namemc": namemc_timing,
            "teun": teun_timing,
            "ckm": coolkidmacho_timing,
            "coolkidmacho": coolkidmacho_timing,
        }.get(self.timing_system, coolkidmacho_timing)(target, self.session)

        await self.snipe(droptime, target, offset)

    # pylint: disable=too-many-locals
    async def snipe(self, droptime, target, offset):

        authentication_coroutines = [
            acc.fully_authenticate(session=self.session)
            for acc in self.accounts
        ]
        pre_snipe_coroutines = [
            acc.snipe_connect()
            for _ in range(self.snipe_requests)
            for acc in self.accounts
        ]  # For later use

        now = time.time()
        time_until_authentication = (
            0
            if now > (droptime - self.start_authentication)
            else (droptime - self.start_authentication) - now
        )

        self.log.debug(
            f"authorizing accounts in {time_until_authentication} seconds.")

        await asyncio.sleep(time_until_authentication)

        await asyncio.gather(*authentication_coroutines)

        for acc in self.accounts:
            acc.encode_snipe_data(target)

        now = time.time()
        time_until_connect = 0 if now > (
            droptime - 32) else (droptime - 32) - now

        self.log.debug(f"Connecting in {time_until_connect} seconds.")

        await asyncio.sleep(time_until_connect)

        await asyncio.gather(*pre_snipe_coroutines)

        snipe_coroutines = [
            acc.snipe(acc.readers_writers[i][1], droptime=droptime)
            for i in range(self.snipe_requests)
            for acc in self.accounts
        ]

        while time.time() < droptime - offset / 1000:
            await asyncio.sleep(0.00001)  # bad timing solution

        await asyncio.gather(*snipe_coroutines)  # Sends the snipe requests
        responses = await asyncio.gather(
            *[
                acc.snipe_read(
                    target, acc.readers_writers[i][0],
                    acc.readers_writers[i][1],
                    droptime=droptime
                )
                for i in range(self.snipe_requests)
                for acc in self.accounts
            ]
        )  # Reads the responses

        for is_success, email, _ in responses:
            if is_success:
                success_acc = util.find_acc_by_email(email, self.accounts)
                self.log.info(
                    f"{self.color.white}[{self.color.l_green}"
                    f"success{self.color.white}]{self.color.reset} "
                    f"sniped {target} onto {success_acc.email}"
                )
                self.log.info(
                    f"If you like this sniper, please consider donating at {self.color.l_green}https://mcsniperpy.com/donate{self.color.reset} :)"
                )
                if self.do_announce:
                    await announce.announce(
                        username=target,
                        authorization=self.announce_code,
                        session=self.session,
                    )
                if len(self.webhook_urls) > 0:
                    webhook_description = await announce.gen_webhook_desc(
                        self.webhook_format, target, self.session
                    )
                    for webhook_url in self.webhook_urls:
                        await announce.webhook_announce(
                            webhook_url,
                            self.session,
                            webhook_description,
                            "New Snipe!",
                            False,
                        )
                if self.change_skin_on_snipe:
                    for acc in self.accounts:
                        await acc.change_skin(
                            self.skin_variant,
                            self.skin,
                            self.skin_change_type,
                            self.session
                        )

    def on_shutdown(self):
        if self.session.session is not None:
            asyncio.run(self.session.session.close())
        if self.log is not None:
            self.log.shutdown()

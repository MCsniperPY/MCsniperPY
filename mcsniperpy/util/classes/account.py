import asyncio
import ssl
import time

from mcsniperpy.util.logs_manager import Color as color
from mcsniperpy.util.logs_manager import Logger as log


class Account:
    def __init__(self, email, password, *sqs, **kwargs):
        if kwargs.get('acc_type') == 'microsoft':
            log.error('MCsniperPY does not support Microsoft accounts at the moment.')
        self.email = email  # email
        self.password = password  # password
        self.sqs = sqs  # security question answers

        self.questions = []  # Actual questions
        self.answer_ids = []  # IDS of the security question answers

        self.username = ""  # Totally useless lol

        self.bearer = ""
        self.headers = {"Authorization": "Bearer TOKEN"}

        self.snipe_data = ("PUT /minecraft/profile/name/NAME HTTP/1.1\r\n"
                           "Host: api.minecraftservices.com\r\n"
                           "Authorization: Bearer TOKEN\r\n"
                           "\r\n").encode()

        self.readers_writers = []

    def encode_snipe_data(self, name):
        self.snipe_data = (f"PUT /minecraft/profile/name/{name} HTTP/1.1\r\n"
                           "Host: api.minecraftservices.com\r\n"
                           f"Authorization: Bearer {self.bearer}\r\n"
                           "\r\n").encode()

    def encode_snipe_data_proxy(self, name):
        self.snipe_data = (f"PUT https://api.minecraftservices.com/minecraft/profile/name/{name} HTTP/1.1\r\n"
                           "Host: api.minecraftservices.com\r\n"
                           f"Authorization: Bearer {self.bearer}\r\n"
                           "\r\n").encode()

    async def authenticate(self, session) -> bool:
        resp, _, resp_json = await session.post(
            "https://authserver.mojang.com/authenticate",
            json={
                "agent": {
                    "name": "Minecraft",
                    "version": 1
                },
                "username": self.email,
                "password": self.password,
                "requestUser": "false"
            },
            headers={"Content-Type": "application/json"}
        )

        if resp.status == 200:
            self.headers["Authorization"] = f"Bearer {resp_json['accessToken']}"  # authorization header
            self.bearer = resp_json['accessToken']
            return True
        return False

    async def get_questions(self, session) -> None:
        resp, _, resp_json = await session.get(
            "https://api.mojang.com/user/security/challenges",
            headers=self.headers
        )

        self.answer_ids = [question["answer"]["id"] for question in resp_json]
        self.questions = [question["question"]["question"] for question in resp_json]

        if resp.status == 200:
            return
        log.error(f"failed to get security questions for {self.email}")

    async def need_sqs(self, session) -> bool:
        resp, _, _ = await session.get(
            "https://api.mojang.com/user/security/location",
            headers=self.headers
        )

        return resp.status == 403

    async def submit_questions(self, session):

        if self.sqs == ():
            log.error(f"security questions for {self.email} not provided!")
            return False

        resp, _, _ = await session.post(
            "https://api.mojang.com/user/security/location",
            headers=self.headers,
            json=[
                {
                    "id": self.answer_ids[0],
                    "answer": self.sqs[0]
                },
                {
                    "id": self.answer_ids[1],
                    "answer": self.sqs[1]
                },
                {
                    "id": self.answer_ids[2],
                    "answer": self.sqs[2]
                }
            ]
        )

        # Yes, that's kinda ugly lol. whatever.

        if resp.status == 204:
            return True
        log.error(f"security questions for {self.email} are incorrect!")
        return False

    async def fully_authenticate(self, session):
        if not await self.authenticate(session):
            log.error(f"failed to auth {self.email}")
            return

        if not await self.need_sqs(session):
            log.info(f"{color.white}[{color.l_green}success{color.white}]{color.reset} authenticated {self.email}")
        else:
            await self.get_questions(session)
            if await self.submit_questions(session):
                log.info(f"{color.white}[{color.l_green}success{color.white}]{color.reset} authed {self.email} with security questions")
            else:
                log.error(f"failed to authenticate {self.email}")

    async def snipe_connect(self) -> None:

        reader, writer = await asyncio.open_connection("api.minecraftservices.com", 443, ssl=ssl.SSLContext(),
                                                       ssl_handshake_timeout=5)
        log.debug(f"Connected on account {self.email}")
        writer.write(self.snipe_data[0:-2])

        await writer.drain()
        self.readers_writers.append((reader, writer))

    async def snipe(self, writer: asyncio.StreamWriter, do_log: bool = True) -> None:
        writer.write(self.snipe_data[-2:])
        await writer.drain()
        if do_log:
            log.info(f"sent request @ {time.time()}")
        # Simpler code 🔽 encompasses all of these snipe* functions
        # async with snipe_session.put("https://api.minecraftservices.com/minecraft/profile/name/%s" % "blah",
        #                              headers={
        #                                  "Authorization": "Bearer %s" % self.bearer, "Content-Type": "application/json
        # ^^^^ THAT LINE IS INVALID YOU NEED A " AT THE END ^^^
        #                              }) as r:
        #     print("[%s] %s @ %5f" % (name, r.status, time.time()))
        #     if r.status == 204:
        #         return True, self.email
        #     else:
        #         return False, None

    async def snipe_read(
            self, name: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, do_log: bool = True) -> (
            bool, str, float):
        resp = await reader.read(12)
        now = time.time()
        status = int(resp[9:12])
        is_success = status < 300

        writer.close()
        await writer.wait_closed()

        if do_log:
            pretty_status = '%s%s%s' % (
                {
                    False: color.l_red,
                    True: color.l_green
                }.get(is_success, color.l_red),
                status,
                color.reset
            )
            pretty_name = '%s%s%s' % (
                color.l_cyan,
                name,
                color.reset
            )

            log.info("[%s] [%s] @ %.10f" % (pretty_name, pretty_status, now))
        return is_success, self.email, now

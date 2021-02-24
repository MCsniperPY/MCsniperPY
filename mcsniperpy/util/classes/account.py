import logging

import aiohttp

from ..logs_manager import Logger as log
from .. import request_manager


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

    def encode_snipe_data(self, name):
        self.snipe_data = (f"PUT /minecraft/profile/name/{name} HTTP/1.1\r\n"
                           "Host: api.minecraftservices.com\r\n"
                           f"Authorization: Bearer {self.bearer}\r\n"
                           "\r\n").encode()

    async def authenticate(self) -> bool:
        resp, resp_json, _ = await session.post(
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
        else:
            return False

    async def get_questions(self) -> None:
        resp, resp_json, _ = await session.get(
            "https://api.mojang.com/user/security/challenges",
            headers=self.headers
        )

        self.answer_ids = [question["answer"]["id"] for question in resp_json]
        self.questions = [question["question"]["question"] for question in resp_json]

        if resp.status == 200:
            return
        else:
            print(f"[err] failed to get security questions for {self.email}")

    @property
    async def need_sqs(self):
        resp, _, _ = await session.get(
            "https://api.mojang.com/user/security/location",
            headers=self.headers
        )

        return resp.status == 403

    async def submit_questions(self):

        if self.sqs == ():
            print(f"[err] security questions for {self.email} not provided!")
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
        else:
            print(f"[err] security questions for {self.email} are incorrect!")
            return False

    async def fully_authenticate(self):
        if not await self.authenticate():
            print(f"[err] failed to auth {self.email}")
            return

        if not await self.need_sqs:
            print(f"[success] authed {self.email}")
        else:
            await self.get_questions()
            if await self.submit_questions():
                print(f"[success] authed {self.email} with security questions")
            else:
                print(f"[err] failed to authenticate {self.email}")

    async def snipe(self, name, snipe_session):
        reader, writer = await asyncio.open_connection("api.minecraftservices.com", 443, ssl=True)

        writer.write(self.snipe_data)

        await writer.drain()

        resp = await reader.read(12)
        status = int(resp[9:12])
        writer.close()
        await writer.wait_closed()
        print("[%s] %s @ %.10f" % (name, status, time.time()))
        return status == 204, self.email
        # Simpler code 🔽
        # async with snipe_session.put("https://api.minecraftservices.com/minecraft/profile/name/%s" % "blah",
        #                              headers={
        #                                  "Authorization": "Bearer %s" % self.bearer, "Content-Type": "application/json"
        #                              }) as r:
        #     print("[%s] %s @ %5f" % (name, r.status, time.time()))
        #     if r.status == 204:
        #         return True, self.email
        #     else:
        #         return False, None

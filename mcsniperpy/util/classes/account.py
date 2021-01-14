import logging

import aiohttp

from .. import logs_manager as log
from .. import request_manager


class Account:
    """
    Represents an account in MCsniperPY
    available attributes:
    `email` str
    `password` str
    `security_questions` list of str
    `acc_type` str (mojang or microsoft)
    """

    def __init__(self, email, password, security_questions=None, acc_type="mojang"):
        if security_questions is None:
            security_questions = []

        self.email = email
        self.password = password
        self.security_questions = security_questions
        # acc_type is to be used for Microsoft or Mojang authentication
        self.acc_type = acc_type  # Not implemented | Create a PR with microsoft authentication if you would like to
        self.session = request_manager.RequestManager(
            aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(limit=300),
                headers={}
            )
        )

        self.bearer = ""

    async def mojang_auth(self):

        r = await self.session.post("https://authserver.mojang.com/authenticate", headers=headers, json={
            "username": self.email,
            "password": self.password
        })

        logging.debug(f"{self.email} : {r.content}")

        if r.status_code != 200:
            log.error(f"{self.email} has an incorrect password.")
            return False

        try:
            self.bearer = r.json()['accessToken']
        except:
            log.error(f"{self.email} failed to get bearer token.")
            return False

        r = requests.get("https://api.mojang.com/user/security/challenges", headers={
            "Authorization": "Bearer " + self.bearer
        })

        if len(r.content) > 3:  # Need security questions
            if len(self.security_questions) == 0:
                log.error(f"{self.email} needs security questions and none were provided.")
                return False

            answers = []
            resp_json = r.json()
            logging.debug(f"{resp_json}")

            try:
                for x in range(3):
                    answers.append({"id": resp_json[x]["answer"]["id"], "answer": self.security_questions[x]})
            except Exception as e:
                print(e)
                log.error(f"{self.email} didn't have enough security questions provided.")
                return False

            logging.debug(f"{answers}")
            r = requests.post("https://api.mojang.com/user/security/location", headers={
                "Authorization": "Bearer " + self.bearer
            }, json=answers)

            if r.status_code != 204:
                logging.debug(f"{r.status_code}")
                log.error(f"{self.email} has incorrect security questions.")
                return False

        if not self.check_name_change():
            log.error(f"{self.email} can't change username.")
            return False

        log.success(f"{self.email} logged in successfully.")
        return True

    def authenticate(self):
        # eventually do ms auth here too
        logged_in = self.mojang_auth()
        return logged_in

    def check_name_change(self) -> bool:
        r = requests.get("https://api.minecraftservices.com/minecraft/profile/namechange", headers={
            "Authorization": "Bearer " + self.bearer
        })

        r = r.json()
        try:
            if not r['nameChangeAllowed']:
                return False
        except:  # will probably only happen with non premium accounts
            return False

        return True

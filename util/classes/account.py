import requests
import util.logs_manager as log


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
        # self.session = RequestManager(
        #     aiohttp.ClientSession(
        #         connector=aiohttp.TCPConnector(limit=300),
        #         headers={}
        #     )
        # )

    def mojang_auth(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }

        r = requests.post("https://authserver.mojang.com/authenticate", headers=headers, json={
            "username": self.email,
            "password": self.password
        })

        if r.status_code != 200:
            log.error(f"{self.email} has an incorrect password.")
            return False

        try:
            bearer = r.json()['accessToken']
            log.info(f"{self.email} logged in successfully.")
        except:
            log.error(f"{self.email} failed to get bearer token.")
            return False

        return True

    def authenticate(self):
        # eventually do ms auth here too
        logged_in = self.mojang_auth()
        return logged_in

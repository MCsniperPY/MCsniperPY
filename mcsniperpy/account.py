import aiohttp
from request_manager import RequestManager
from logs_manager import Color
import logs_manager as log


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
        self.security_question = security_question

        # acc_type is to be used for Microsoft or Mojang authentication
        self.acc_type = acc_type  # Not implemented | Create a PR with microsoft authentication if you would like to
        self.session = RequestManager(
            aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(limit=300),
                headers={}
            )
        )

    async def authenticate(self):
        log.debug(f"started authentication for {self.pretty_email}")

    @propety
    async def is_fully_authenticated(self) -> bool:
        resp = await session.get("https://api.mojang.com/user/security/location")
        return resp.ok

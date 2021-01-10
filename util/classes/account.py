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

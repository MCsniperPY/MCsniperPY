try:
    import requests
    from colorama import Fore
    from fake_useragent import UserAgent
    from src.util import custom_info
    from time import time
    from datetime import datetime
    import aiohttp
except:
    import aiohttp
    import requests
    from colorama import Fore
    from fake_useragent import UserAgent
    from util import custom_info
    from time import time
    from datetime import datetime


# def authenticate(config):
#     authenticate_json = {"agent": {"name": "Minecraft", "version": 1}, "username": config['email'], "password": config['password']}
#     headers = {"User-Agent": ua.random, "Content-Type": "application/json"}
#     r = requests.post("https://authserver.mojang.com/authenticate", json=authenticate_json, headers=headers)
#     try:
#         uuid = r.json()["selectedProfile"]["id"]
#     except KeyError:
#         uuid = "unpaid_acc"
#     return r.json()["accessToken"], uuid


# def get_questions(config):
#     auth = {"Authorization": "Bearer: " + config["bearer"]}
#     questions = requests.get("https://api.mojang.com/user/security/challenges", headers=auth)
#     questions = questions.json()
#     try:
#         if questions["errorMessage"] == "The request requires user authentication":
#             print("Bearer didn't work...")

#     except TypeError:
#         return questions, auth


# def validate(token):
#     r = requests.post("https://authserver.mojang.com/validate", json={"accessToken": token}, headers={"User-Agent": ua.random, "Content-Type": "application/json"})
#     if r.status_code != 204:
#         print(Fore.RED, "Failed to authenticate", Fore.RESET)


# def acc_setup(config, questions, auth):
#     answers = []
#     if len(questions) == 0:
#         return

#     for i in range(3):
#         answers.append({"id": questions[i]["answer"]["id"], "answer": config["questions"][i]})
#     post_answers = requests.post("https://api.mojang.com/user/security/location", json=answers, headers=auth)
#     if post_answers.status_code != 204:
#         print(f"{Fore.RED} Failed: {post_answers.text} {Fore.RESET}")
#     else:
#         custom_info(f"{Fore.GREEN}credentials for {config['email']} verified{Fore.RESET}")


# def no_questions_full_auth(config):
#     config["bearer"], uuid = authenticate(config)
#     _, auth = get_questions(config)
#     validate(config["bearer"])
#     return uuid, auth


# def full_auth(config):
#     config["bearer"], uuid = authenticate(config)
#     qs, auth = get_questions(config)
#     acc_setup(config, qs, auth)
#     validate(config["bearer"])
#     return uuid, auth


class Account():
    """This is an account class which can authenticate a mojang account given an email, password, and optional security questions"""

    def __init__(self, email, password, questions=[]):
        self.email = email
        self.password = password
        if questions == [] or questions == ['', '', '']:
            self.has_questions = False
            self.questions = questions
        elif len(questions) == 3:
            self.has_questions = True
            self.question_answers = questions
        else:
            print("i have no idea what went wrong...")
        self.statuses = []

    def questions_authenticate(self):
        self.block_snipe_words = ["block", "snipe"]
        ua = UserAgent()
        authenticate_json = {"agent": {"name": "Minecraft", "version": 1}, "username": self.email, "password": self.password}
        headers = {"User-Agent": ua.random, "Content-Type": "application/json"}
        r = requests.post("https://authserver.mojang.com/authenticate", json=authenticate_json, headers=headers)
        self.statuses.append(r.status_code)
        try:
            self.uuid = r.json()["selectedProfile"]["id"]
        except KeyError:
            self.uuid = "unpaid_acc"
        try:
            self.access_token = r.json()["accessToken"]
        except KeyError:
            custom_info(f"{Fore.RED}Failed to authenticate {self.email}: {r.json()['errorMessage']}{Fore.RESET}")
            return
        self.auth = {"Authorization": "Bearer: " + self.access_token}
        questions = requests.get("https://api.mojang.com/user/security/challenges", headers=self.auth)
        self.statuses.append(r.status_code)
        try:
            if questions["errorMessage"] == "The request requires user authentication":
                custom_info(f"{Fore.RED}There was a problem with authentication{Fore.RESET}")
        except TypeError:
            self.questions = questions.json()
        answers = []

        for x in range(3):
            answers.append({"id": self.questions[x]["answer"]["id"], "answer": self.question_answers[x]})
        post_answers = requests.post("https://api.mojang.com/user/security/location", json=answers, headers=self.auth)
        self.statuses.append(r.status_code)
        if post_answers.status_code != 204:
            print(f"{Fore.RED} Failed: {post_answers.text} {Fore.RESET}")
            return
        r = requests.post("https://authserver.mojang.com/validate", json={"accessToken": self.access_token}, headers={"User-Agent": ua.random, "Content-Type": "application/json"})
        self.statuses.append(r.status_code)
        if r.status_code != 204:
            custom_info(f"{Fore.RED}Failed to authenticate {self.email}: {r.json()['errorMessage']}{Fore.RESET}")
            return
        else:
            custom_info(f"{Fore.GREEN}credentials for {self.email} verified {str(self.statuses).replace(', ', ' ').replace('[', '').replace(']', '')} | {self.auth['Authorization'][-10:-1]}{Fore.RESET}")

    def no_questions_authenticate(self):
        self.block_snipe_words = ["block", "snipe"]
        ua = UserAgent()
        authenticate_json = {"agent": {"name": "Minecraft", "version": 1}, "username": self.email, "password": self.password}
        headers = {"User-Agent": ua.random, "Content-Type": "application/json"}
        r = requests.post("https://authserver.mojang.com/authenticate", json=authenticate_json, headers=headers)
        self.statuses.append(r.status_code)
        try:
            self.uuid = r.json()["selectedProfile"]["id"]
        except KeyError:
            self.uuid = "unpaid_acc"
        try:
            self.access_token = r.json()["accessToken"]
        except KeyError:
            custom_info(f"{Fore.RED}Failed to authenticate {self.email}: {r.json()}{Fore.RESET}")
            return
        self.auth = {"Authorization": "Bearer: " + self.access_token}
        r = requests.post("https://authserver.mojang.com/validate", json={"accessToken": self.access_token}, headers={"User-Agent": ua.random, "Content-Type": "application/json"})
        self.statuses.append(r.status_code)
        if r.status_code != 204:
            custom_info(f"{Fore.RED}Failed to authenticate {self.email}: {r.json()['errorMessage']}{Fore.RESET}")
            return
        r = requests.get("https://api.mojang.com/user/security/challenges", headers={"Authorization": "Bearer " + self.access_token})
        self.statuses.append(r.status_code)
        if r.status_code == 200:
            custom_info(f"{Fore.GREEN}credentials for {self.email} verified | {str(self.statuses).replace(', ', ' ').replace('[', '').replace(']', '')} | {self.auth['Authorization'][-10:-1]}{Fore.RESET}")
        else:
            custom_info(f"{Fore.RED}Failed to authenticate {self.email}:{r.json()}{Fore.RESET}")
            return

    def authenticate(self):
        if self.has_questions:
            self.questions_authenticate()
        elif not self.has_questions:
            self.no_questions_authenticate()
        self.statuses = []

    async def send_request(self, block_snipe, target_username, logging_y_n, session):
        start = time()
        if block_snipe == 0:
            # r = requests.put(f"https://api.mojang.com/user/profile/agent/minecraft/name/{target_username}", headers=self.auth)
            async with session.put("https://api.mojang.com/user/profile/agent/minecraft/name/%s" % target_username, headers=self.auth) as r:
                await r.read()
                if logging_y_n:
                    if r.status == 404 or r.status == 400:
                        print(f"{Fore.RED} [ERROR] | Failed to {self.block_snipe_words[block_snipe]} name | {r.status}", str(time() - start)[0:10], "|", datetime.now())
                    elif r.status == 204 or r.status == 200:
                        print(f"{Fore.GREEN} [SUCCESS] | {self.block_snipe_words[block_snipe].rstrip('e')}ed {target_username} onto {self.email} | {r.status}", str(time() - start)[0:10], "|", datetime.now())
                    elif r.status == 401:
                        print(f"{Fore.RED} [ERROR] | REQUEST NOT AUTHENTICATED OR RATELIMIT | {r.status}", str(time() - start)[0:10], "|", datetime.now())
                    else:
                        print(f"{Fore.RED} [ERROR] | IDK | {r.status}", str(time() - start)[0:10], "|", datetime.now())
                else:
                    if r.status == 204:
                        print(f"{Fore.GREEN} [SUCCESS] | {self.block_snipe_words[block_snipe].rstrip('e')}ed {target_username} onto {self.email} | {r.status}", str(time() - start)[0:10], "|", datetime.now())
        # else:
        #     print(f"{Fore.GREEN} [SUCCESS] | {self.block_snipe_words[block_snipe].rstrip('e')}ed {target_username} onto {self.email} | {r.status}", str(time() - start)[0:10], "|", datetime.now())
        elif block_snipe == 1:
            # r = requests.post(f"https://api.mojang.com/user/profile/{self.uuid}/name", headers=self.auth, json={"name": target_username, "password": self.password})
            async with session.post("https://api.mojang.com/user/profile/%s/name" % (self.uuid), headers=self.auth, json={"name": target_username, "password": self.password}) as r:
                await r.read()
                if logging_y_n:
                    if r.status == 404 or r.status == 400:
                        print(f"{Fore.RED} [ERROR] | Failed to {self.block_snipe_words[block_snipe]} name | {r.status}", str(time() - start)[0:10], "|", datetime.now())
                    elif r.status == 204 or r.status == 200:
                        print(f"{Fore.GREEN} [SUCCESS] | {self.block_snipe_words[block_snipe].rstrip('e')}ed {target_username} onto {self.email} | {r.status}", str(time() - start)[0:10], "|", datetime.now())
                    elif r.status == 401:
                        print(f"{Fore.RED} [ERROR] | REQUEST NOT AUTHENTICATED OR RATELIMIT | {r.status}", str(time() - start)[0:10], "|", datetime.now())
                    else:
                        print(f"{Fore.RED} [ERROR] | IDK | {r.status}", str(time() - start)[0:10], "|", datetime.now())
                else:
                    if r.status == 204:
                        print(f"{Fore.GREEN} [SUCCESS] | {self.block_snipe_words[block_snipe].rstrip('e')}ed {target_username} onto {self.email} | {r.status}", str(time() - start)[0:10], "|", datetime.now())
        else:
            r = requests.put(f"https://api.mojang.com/user/profile/agent/minecraft/name/{target_username}", headers=self.auth)
        


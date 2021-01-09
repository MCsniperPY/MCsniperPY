from utils import *

import asyncio
from datetime import datetime, timezone
import logging
import time
import utils

try:
    from colorama import Fore, init
except ImportError:
    print("You are missing the required modules | Please refer to the usage on how to install")
    quit()

init()
logging.basicConfig(level=logging.INFO, format='%(message)s')

class Account:
    def __init__(self, email, password, questions=[]):
        self.email = email
        self.password = password
        self.questions = questions
        self.got_name = False
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"
        self.failed_auth = False
        self.authenticate_json = {"username": self.email, "password": self.password}
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0", "Content-Type": "application/json"}

    async def authenticate(self, session, sleep_time, block_snipe):
        await asyncio.sleep(sleep_time)
        # custom_info(f"{Fore.WHITE}starting auth for {self.email}")
        debug_mode = False
        async with session.post("https://authserver.mojang.com/authenticate", json=self.authenticate_json, headers=self.headers) as r:
            if check_resp(r.status):
                resp_json = await r.json()
                try:
                    self.uuid = resp_json["selectedProfile"]["id"]
                except KeyError:
                    if debug_mode:
                        print(resp_json)
                    else:
                        if block_snipe == 2:
                            custom_info(f"{self.email} is unpaid and cannot snipe names. {Fore.RED}YOU ARE SNIPING. This will fail.{Fore.RESET}")
                self.auth = {"Authorization": "Bearer: " + resp_json["accessToken"]}
                self.access_token = resp_json["accessToken"]
            else:
                resp_error(f"invalid credentials | {self.email}")
                self.failed_auth = True
                return
        async with session.get("https://api.mojang.com/user/security/challenges", headers=self.auth) as r:
            answers = []
            if check_resp(r.status):
                resp_json = await r.json()
                if resp_json == []:
                    async with session.get("https://api.minecraftservices.com/minecraft/profile/namechange", headers={"Authorization": "Bearer " + self.access_token}) as ncE:
                        ncjson = await ncE.json()
                        try:
                            if ncjson['nameChangeAllowed'] is False:
                                logging.info(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}] {self.email} is not eligible for a name change!")
                                self.failed_auth = True
                            else:
                                logging.info(f"{Fore.WHITE}[{Fore.GREEN}SUCCESS{Fore.WHITE}] Logged into {self.email} successfully!")
                        except Exception:
                            logging.info(f"{Fore.WHITE}[{Fore.GREEN}SUCCESS{Fore.WHITE}] Logged into {self.email} successfully!")
                else:
                    try:
                        for x in range(3):
                            answers.append({"id": resp_json[x]["answer"]["id"], "answer": self.questions[x]})
                    except IndexError:
                        logging.info(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}]{Fore.RESET} {self.email} has security questions and you did not provide any!")
                        self.failed_auth = True
                        return
                    async with session.post("https://api.mojang.com/user/security/location", json=answers, headers=self.auth) as r:
                        if check_resp(r.status):
                            logging.info(f"{Fore.WHITE}[{Fore.GREEN}success{Fore.WHITE}]{Fore.GREEN} signed in to {self.email}{Fore.RESET}")
                        else:
                            resp_error(f"security questions incorrect | {self.email}")
                            self.failed_auth = True
            else:
                logging.info(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}]{Fore.RESET} {self.email} something went wrong with authentication for {self.email}! | {r.status}")
                self.failed_auth = True

    async def block_req(self, session, target_username):
        await asyncio.sleep(0)
        try:
            async with session.put(f"https://api.mojang.com/user/profile/agent/minecraft/name/{target_username}", headers=self.auth) as response:
                utils.sent_reqs += 1
                now = datetime.now()
                await response.read()
                if response.status == 204:
                    logging.info(f"{Fore.WHITE}[{Fore.GREEN}SUCCESS{Fore.WHITE}] | Blocked {Fore.CYAN}{target_username}{Fore.WHITE} on {self.email} | {Fore.GREEN}{response.status}{Fore.WHITE} @ {Fore.CYAN}{now}{Fore.RESET}")
                    asyncio.get_event_loop().stop()
                else:
                    logging.info(f"{Fore.WHITE}[{Fore.RED}error{Fore.WHITE}] {Fore.RED} {response.status} {Fore.WHITE}@{Fore.CYAN} {now}{Fore.RESET}")
        except AttributeError:
            print(f'{Fore.WHITE}[{Fore.RED}error{Fore.WHITE}]{Fore.RESET} {self.email} failed authentication and cannot snipe!')

    async def snipe_req(self, session, target_username):
        await asyncio.sleep(0)
        try:
            async with session.post(f"https://api.mojang.com/user/profile/{self.uuid}/name", headers=self.auth, json={"name": target_username, "password": self.password}) as response:
                now = datetime.now()
                utils.sent_reqs += 1
                await response.read()
                if response.status == 204:
                    logging.info(f"{Fore.WHITE}[{Fore.GREEN}SUCCESS{Fore.WHITE}] | Sniped {Fore.CYAN}{target_username}{Fore.WHITE} on {self.email} | {Fore.GREEN}{response.status}{Fore.WHITE} @ {Fore.CYAN}{now}{Fore.RESET}")
                    self.got_name = True
                    if config.change_skin:
                        await self.authenticate(session, 1, 1)
                    asyncio.get_event_loop().stop()
                else:
                    logging.info(f"{Fore.WHITE}[{Fore.RED}error{Fore.WHITE}] {Fore.RED} {response.status} {Fore.WHITE}@{Fore.CYAN} {now}{Fore.RESET}")
        except AttributeError:
            print(f'{Fore.WHITE}[{Fore.RED}error{Fore.WHITE}]{Fore.RESET} {self.email} failed authentication and cannot snipe!')

    def webhook_skin_write_file(self, block_snipe):
        time.sleep(1)
        with requests.session() as session:
            with open("success.txt", "a") as f:
                f.write(f"{self.email}:{self.password} - {target_username}\n")
            if config.change_skin:
                files = {"model": config.skin_model, "url": config.skin}
                auth = self.auth
                auth["Content-Type"] = "application/x-www-form-urlencoded"
                with session.post(f"https://api.mojang.com/user/profile/{self.uuid}/skin", headers=self.auth, data=files) as r:
                    if r.status_code == 204 or r.status_code == 200:
                        logging.info(f"{Fore.WHITE}[{Fore.GREEN}success{Fore.WHITE}]{Fore.RESET} changed skin of {self.email}")
                    else:
                        logging.info(f"{Fore.WHITE}[{Fore.RED}FAIL{Fore.WHITE}]{Fore.RESET} Failed to change skin {self.email} | {str(r.status_code)}")
                        logging.info(r.json())
            else:
                custom_info(f"not changing skin | {self.email}")
            for hook in config.webhooks:
                with session.post(hook, json={"embeds": [{"title": "New Snipe 🎉", "description": f"Sniped `{target_username}` with {searches} searches using [MCsniperPY](https://github.com/Kqzz MCsniperPY)!", "color": 16744192}]}) as r:
                    if r.status_code == 200 or r.status_code == 204:
                        logging.info(f"{Fore.WHITE}[{Fore.GREEN}success{Fore.WHITE}]{Fore.RESET} sent webhook of snipe!")
                    else:
                        logging.info(r.status_code_code)
                        logging.info(r.json())
            if len(config.webhooks) == 0:
                custom_info("No discord webhooks detected | paste a webhook into config.txt with \"wh:\" before it")
            try:
                with session.post("https://announcements-api.herokuapp.com/api/v1/announce", json={"name": target_username.strip()}, headers={"Authorization": config.custom_announce}) as r:
                    if r.status_code == 204:
                        logging.info(f"{Fore.WHITE}[{Fore.GREEN}success{Fore.WHITE}]{Fore.RESET} sent custom announcement of snipe!")
                    else:
                        logging.info(f"{Fore.RED} {r.status_code} | Failed to send custom announcement!{Fore.RESET}")
                        print(r.json())
            except AttributeError as e:
                custom_info(f"No custom announcement detected | {e}")
                custom_info("type >generate in #bot-commands in the discord to announce your snipes")

from config import Config
from utils import *
from timing import *

try:
    import aiohttp
    import logging
    from colorama import Fore, init
    from datetime import datetime, timezone
    import os
    import asyncio
    from os import path
    import time
    from bs4 import BeautifulSoup
    import sys
    import requests
except ImportError:
    print("You are missing the required modules | Please refer to the usage on how to install")
    quit()

init()

logging.basicConfig(level=logging.INFO, format='%(message)s')
times = []
global sent_reqs
sent_reqs = 0


def menu(options):
    i = 1
    # loop through options and print
    custom_info(f"select a number 1 - {len(options)}")
    for option in options:
        print(f"{i}). {option}")
        i += 1
    # main function loop
    # Doesn't end until a correct answer is given
    while True:
        try:
            # takes an input using readchar's readkey function
            choice = int(input("> "))
            options[choice - 1]
            # returns the option the user selected by list index
            return choice - 1
        except (ValueError, IndexError):
            print("please enter a valid option")


async def time_snipe(target, block_snipe):
    if config.timing == "api":
        try:
            timing = await mojang_timing(target, block_snipe)
        except Exception:
            try:
                timing = await nx_timing(target, block_snipe)
            except Exception:
                try:
                    timing = await namemc_timing(target, block_snipe)
                except Exception:
                    print(f"{Fore.WHITE}[{Fore.RED}{Fore.RED}]{Fore.RESET} Failed to time snipe")
    elif config.timing == "namemc":
        try:
            timing = await namemc_timing(target, block_snipe)
        except Exception as e:
            resp_error(f"failed to time snipe | retrying | {e}")
            try:
                timing = await nx_timing(target, block_snipe)
            except Exception as e:
                resp_error(f"failed to time snipe | retrying | {e}")
                try:
                    timing = await mojang_timing(target, block_snipe)
                except Exception:
                    print(f"{Fore.WHITE}[{Fore.RED}{Fore.RED}]{Fore.RESET} Failed to time snipe")
    else:
        print("Failed to detect timing system | using default")
        try:
            timing = await mojang_timing(target, block_snipe)
        except Exception:
            print("failed to time snipe | retrying")
            try:
                timing = await nx_timing(target, block_snipe)
            except Exception:
                print("failed to time snipe | retrying")
                try:
                    timing = await namemc_timing(target, block_snipe)
                except Exception:
                    print(f"{Fore.WHITE}[{Fore.RED}{Fore.RED}]{Fore.RESET} Failed to time snipe")
    return timing


class Account:
    def __init__(self, email, password, questions=[]):
        self.email = email
        self.password = password
        self.questions = questions
        self.got_name = False
        self.failed_auth = False
        self.authenticate_json = {"agent": {"name": "Minecraft", "version": 1}, "username": self.email, "password": self.password}
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.3", "Content-Type": "application/json"}

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
                    logging.info(f"{Fore.WHITE}[{Fore.GREEN}success{Fore.WHITE}]{Fore.GREEN} signed in to {self.email}{Fore.RESET}")
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

    async def block_req(self, session, ctarget_username):
        await asyncio.sleep(0)
        try:
            async with session.put(f"https://api.mojang.com/user/profile/agent/minecraft/name/{target_username}", headers=self.auth) as response:
                global sent_reqs
                sent_reqs += 1
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
                global sent_reqs
                sent_reqs += 1
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
                with session.post(hook, json={"embeds": [{"title": "New Snipe 🎉", "description": f"Sniped `{target_username}` with [MCsniperPY](https://github.com/Kqzz/MCsniperPY)!", "color": 65395}]}) as r:
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


# async def get_name_of_the_week():
#     async with aiohttp.ClientSession() as session:
#         async with session.get("https://announcements-api.herokuapp.com/api/v1/nameoftheweek") as r:
#             name_json = await r.json()
#             name = name_json["name"]
#             custom_info(f"Opening {name} in namemc!")
#             try:
#                 webbrowser.open_new_tab(f"https://namemc.com/name/{name}")
#                 custom_input("press enter to quit: ")
#             except Exception:
#                 print("failed to open name!")
#                 custom_input("press enter to quit: ")


def gather_info():
    block_snipe = menu(options=["Snipe name", "Block name"])
    target_username = custom_input(f"What name would you like to {['snipe', 'block'][block_snipe]}: ")
    try:
        delay = int(custom_input("Custom delay in ms: "))
    except ValueError:
        print('thats not a valid number')
    return block_snipe, target_username, delay


def load_accounts_file():
    accounts = []
    if not path.exists("accounts.txt"):
        print(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}]{Fore.RESET} accounts.txt not found | creating one")
        open('accounts.txt', 'w+')
        input("Press enter to reload accounts. ")
        load_accounts_file()
    else:
        accounts = open('accounts.txt').readlines()
        if len(accounts) == 0:
            print(f"Accounts not found in accounts.txt file please add accounts with format (email:pass) or (email:pass:q1:q2:q3)")
            input("Press any key to reload accounts.")
            load_accounts_file()
        if len(accounts) > config.max_accs:
            print(f"{Fore.WHITE}[{Fore.YELLOW}warning{Fore.WHITE}]{Fore.RESET} you inputted too many accounts | removing {len(accounts) - config.max_accs}")
            accounts = accounts[0:30]
    return accounts


def load_accounts():
    accounts = []
    for acc in load_accounts_file():
        acc = acc.rstrip().split(":")
        if acc == ['']:
            continue
        try:
            accounts.append(Account(acc[0], acc[1], [acc[2], acc[3], acc[4]]))
        except IndexError:
            accounts.append(Account(acc[0], acc[1]))
    return accounts


class session:
    block_snipe = ["Snipe", "block"]

    def __init__(self, target_username, accounts, block_snipe, snipe_delay):
        self.target_username = target_username
        self.accounts = accounts
        self.block_snipe = block_snipe
        self.snipe_delay = snipe_delay
        loop = asyncio.get_event_loop()
        self.drop_time = loop.run_until_complete(time_snipe(self.target_username, self.block_snipe))
        try:
            self.setup_time = self.drop_time - 55
        except Exception:
            resp_error(f"Cannot snipe name {target_username}")
            time.sleep(2)
            quit()
        self.setup = False
        self.ran = False
        self.drop_time = self.drop_time - snipe_delay / 1000

    def run(self):
        loop = asyncio.get_event_loop()
        while True:
            now = time.time()
            if now >= self.drop_time and not self.ran:
                try:
                    start = time.time()
                    loop.run_until_complete(self.send_requests())
                except RuntimeError:
                    pass
                end = time.time()
                elapsed_time = end - start
                for acc in self.accounts:
                    if acc.got_name:
                        time.sleep(2)
                        acc.webhook_skin_write_file(self.block_snipe)
                rq_sec = sent_reqs / elapsed_time
                times.append(rq_sec)
                logging.info(f"{Fore.GREEN}{str(sum(times))[0:13]}{Fore.CYAN} rqs/sec (ESTIMATE) {Fore.WHITE}|{Fore.CYAN} Took {Fore.WHITE}{str(elapsed_time)[0:8]}{Fore.CYAN} seconds{Fore.RESET} | {sent_reqs} requests")
                try:
                    if len(sys.argv) < 3:
                        custom_input("press enter to quit: ")
                    return
                except Exception:
                    return
            elif now >= self.setup_time and not self.setup:
                loop.run_until_complete(self.run_auth())
                for acc in accounts:
                    if acc.failed_auth:
                        # logging.info(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}] Removing account: {acc.email} | auth failed")
                        accounts.remove(acc)
                if len(accounts) == 0:
                    logging.info(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}] you have 0 accounts available to snipe on! | quitting program...")
                    quit()
                custom_info("setup complete")
                self.setup = True
            time.sleep(.00001)

    async def webhook_skin_file(self, acc):
        await acc.webhook_skin_write_file()

    async def send_requests(self):
        async with aiohttp.ClientSession() as session:
            if self.block_snipe == 0:
                self.coros = [
                    acc.snipe_req(session, self.target_username) for acc in self.accounts for _ in range(config.snipe_reqs)
                ]
            elif self.block_snipe == 1:
                self.coros = [
                    acc.block_req(session, self.target_username) for acc in self.accounts for _ in range(config.block_reqs)
                ]
            await asyncio.wait(self.coros)

    async def run_auth(self):
        async with aiohttp.ClientSession() as session:
            coros = [
                acc.authenticate(session, self.accounts.index(acc) * (config.auth_delay / 1000), self.block_snipe) for acc in self.accounts
            ]
            await asyncio.wait(coros)


if __name__ == '__main__':
    print_title()
    config = Config()
    accounts = load_accounts()
    try:
        target_username = sys.argv[1]
        block_snipe = sys.argv[2]
        if str(block_snipe).lower() == "snipe" or str(block_snipe) == "0":
            block_snipe = 0
        if str(block_snipe).lower() == "block" or str(block_snipe) == "1":
            block_snipe = 1
        try:
            snipe_delay = int(sys.argv[3])
        except IndexError:
            if block_snipe == 0:
                snipe_delay = 900
            else:
                snipe_delay = 200
    except IndexError:
        block_snipe, target_username, snipe_delay = gather_info()
    session = session(target_username, accounts, block_snipe, snipe_delay)
    session.run()

import aiohttp
import logging
from colorama import Fore, init
from datetime import datetime, timedelta
import asyncio
from os import path
import time
from bs4 import BeautifulSoup
import json
import sys

init()

logging.basicConfig(level=logging.INFO, format='%(message)s')
times = []


def custom_info(message):
    logging.info(f"{Fore.BLUE}[info] {Fore.RESET}{message}")


def print_title():
    print(f"""

{Fore.CYAN}┌──────────────────────────────────────────────────────────────────────────────────────┐
{Fore.CYAN}│{Fore.RESET} ███╗   ███╗ ██████╗███████╗███╗   ██╗██╗██████╗ ███████╗██████╗ {Fore.BLUE}██████╗ ██╗   ██╗
{Fore.CYAN}│{Fore.RESET} ████╗ ████║██╔════╝██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗{Fore.BLUE}██╔══██╗╚██╗ ██╔╝
{Fore.CYAN}│{Fore.RESET} ██╔████╔██║██║     ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝{Fore.BLUE}██████╔╝ ╚████╔╝{Fore.CYAN}     |
|{Fore.RESET} ██║╚██╔╝██║██║     ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗{Fore.BLUE}██╔═══╝   ╚██╔╝     {Fore.CYAN} │
{Fore.RESET}  ██║ ╚═╝ ██║╚██████╗███████║██║ ╚████║██║██║     ███████╗██║  ██║{Fore.BLUE}██║        ██║      {Fore.CYAN} │
{Fore.RESET}  ╚═╝     ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝{Fore.BLUE}╚═╝        ╚═╝      {Fore.CYAN} │
{Fore.CYAN}└──────────────────────────────────────────────────────────────────────────────────────┘
{Fore.GREEN}Developed by @Kqzz#0001 on Discord {Fore.BLUE}| Discord server: https://discord.gg/jZm4qNF
{Fore.GREEN}THIS SNIPER IS 100% FREE ON GITHUB""", Fore.RESET)


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


def custom_input(message):
    print(f"{Fore.BLUE}[input] {Fore.RESET}", end='')
    input_return = input(message)
    return input_return


def check_resp(status):
    if str(status)[0] == str(2):
        return True
    else:
        return False


def resp_error(message):
    print(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}] {message}")


# def get_proxies():
#     with open("working.txt", "r") as f:
#         prox = f.readlines()
#         proxies = []
#         for proxy in prox:
#             proxies.append(proxy.strip())
#         return proxies


async def time_snipe(target, block_snipe):
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    now = datetime.strptime(now, '%Y-%m-%dT%H:%M:%S')
    block_snipe_words = ["snipe", "block"]
    async with aiohttp.ClientSession() as session:
        try:
            # namemc_url = f"https://namemc.com/search?q={target}"
            try:
                async with session.get(f"https://namemc.com/search?q={target}") as page:
                    # page = requests.get(namemc_url)
                    soup = BeautifulSoup(await page.text(), 'html.parser')
                    snipe_time = soup.find("time", {"id": "availability-time"}).attrs["datetime"]
                    snipe_time = datetime.strptime(snipe_time, '%Y-%m-%dT%H:%M:%S.000Z')
            except AttributeError:
                logging.info(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}]{Fore.RESET} you were blocked by namemc or  retrying.")
                await asyncio.sleep(10)
                async with session.get(f"https://namemc.com/search?q={target}") as page:
                    # page = requests.get(namemc_url)
                    soup = BeautifulSoup(await page.text(), 'html.parser')
                    snipe_time = soup.find("time", {"id": "availability-time"}).attrs["datetime"]
                    snipe_time = datetime.strptime(snipe_time, '%Y-%m-%dT%H:%M:%S.000Z')
        except AttributeError:
            status_bar = soup.find(id="status-bar")
            info = status_bar.find_all("div", class_="col-sm-6 my-1")
            status = info[0].text.split("\n")[2]
            if status.lower().rstrip('*') == 'available':
                snipe_time = custom_input("At what time will this name be able to be turboed (month/day/yr, 24hrtime_hour:minute:second) (UTC)\nexample: 03/06/2020 01:06:45\n» ")
                snipe_time = datetime.strptime(snipe_time.strip(), "%m/%d/%Y %H:%M:%S")
                wait_time = snipe_time - now
                wait_time = wait_time.seconds / 60
                custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in {wait_time} minutes | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
                return snipe_time
            print(f"\"{target}\" is {status}. The sniper cannot claim names that are {status} so go claim it fast through https://my.minecraft.net if possible.")
            quit()

        wait_time = snipe_time - now
        wait_time = wait_time.seconds
        custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in {wait_time} seconds | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
        return snipe_time


class Account:
    def __init__(self, email, password, questions=[]):
        self.email = email
        self.password = password
        self.questions = questions
        self.got_name = False
        self.failed_auth = False
        self.authenticate_json = {"agent": {"name": "Minecraft", "version": 1}, "username": self.email, "password": self.password}
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.3", "Content-Type": "application/json"}

    async def authenticate(self, session):
        # logging.info(f"{Fore.WHITE}[{Fore.CYAN}INFO{Fore.WHITE}]{Fore.RESET} starting auth for {Fore.CYAN}{self.email}{Fore.RESET}")
        debug_mode = json.loads(open("settings.json", "r").read())["debug_mode"]
        async with session.post("https://authserver.mojang.com/authenticate", json=self.authenticate_json, headers=self.headers) as r:
            if check_resp(r.status):
                resp_json = await r.json()
                try:
                    self.uuid = resp_json["selectedProfile"]["id"]
                except KeyError:
                    if debug_mode:
                        print(resp_json)
                    else:
                        custom_info(f"{self.email} is unpaid and cannot snipe names. please make sure you are blocking.")
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
                        return
                    async with session.post("https://api.mojang.com/user/security/location", json=answers, headers=self.auth) as r:
                        if check_resp(r.status):
                            logging.info(f"{Fore.WHITE}[{Fore.GREEN}success{Fore.WHITE}]{Fore.GREEN} signed in to {self.email}{Fore.RESET}")
                        else:
                            resp_error(f"security questions incorrect | {self.email}")
                            self.failed_auth = True
            else:
                logging.info(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}]{Fore.RESET} {self.email} something went wrong with authentication for {self.email}!")
                self.failed_auth = True

    async def block_req(self, session, ctarget_username):
        await asyncio.sleep(0)
        # logging.info(f'{Fore.WHITE}[{Fore.GREEN}SUCCESS{Fore.WHITE}] Sent Request @ {Fore.CYAN}{datetime.now()}')
        async with session.put(f"https://api.mojang.com/user/profile/agent/minecraft/name/{target_username}", headers=self.auth) as response:
            now = datetime.now()
            logging.info(f"{Fore.WHITE}[{f'{Fore.GREEN}SUCCESS' if response.status == 204 else f'{Fore.RED}FAIL'}{Fore.WHITE}]{Fore.RESET}{' ' + target_username + ' ' + Fore.GREEN + self.email if str(response.status)[0] == str(2) else Fore.RED} | {response.status}{Fore.RESET} @ {Fore.CYAN}{now}{Fore.RESET}")
            await response.read()
            if response.status == 204:
                asyncio.get_event_loop().stop()

    async def snipe_req(self, session, target_username):
        await asyncio.sleep(0)
        # logging.info(f'{Fore.WHITE}[{Fore.GREEN}SUCCESS{Fore.WHITE}] Sent Request @ {Fore.CYAN}{datetime.now()}')
        try:
            async with session.post(f"https://api.mojang.com/user/profile/{self.uuid}/name", headers=self.auth, json={"name": target_username, "password": self.password}) as response:
                now = datetime.now()
                logging.info(f"{Fore.WHITE}[{f'{Fore.GREEN}SUCCESS' if response.status == 204 else f'{Fore.RED}FAIL'}{Fore.WHITE}]{Fore.RESET}{' ' + target_username + ' ' + Fore.GREEN + self.email if str(response.status)[0] == str(2) else Fore.RED} | {response.status}{Fore.RESET} @ {Fore.CYAN}{now}{Fore.RESET}")
                await response.read()
                if response.status == 204:
                    self.got_name = True
                    asyncio.get_event_loop().stop()
        except AttributeError:
            print(f'{Fore.WHITE}[{Fore.RED}error{Fore.WHITE}]{Fore.RESET} {self.email} failed authentication and cannot snipe!')

    async def webhook_skin_write_file(self):
        async with aiohttp.ClientSession() as session:
            with open("success.txt", "a") as f:
                f.write(f"{self.email}:{self.password} - {target_username}\n")
            try:
                files = {"model": "slim", "url": open("skin.txt", "r").read().strip()}
                auth = self.auth
                auth["Content-Type"] = "application/x-www-form-urlencoded"
                async with session.post(f"https://api.mojang.com/user/profile/{self.uuid}/skin", headers=self.auth, data=files) as r:
                    if r.status == 204 or r.status == 200:
                        logging.info(f"{Fore.WHITE}[{Fore.GREEN}success{Fore.WHITE}]{Fore.RESET} changed skin of {self.email}")
                    else:
                        logging.info(f"{Fore.WHITE}[{Fore.RED}FAIL{Fore.WHITE}]{Fore.RESET} Failed to change skin {self.email} | {r.status}")
                        logging.info(await r.json())
            except FileNotFoundError:
                pass
            except:
                logging.info(f"{Fore.WHITE}[{Fore.RED}i have no idea{Fore.WHITE}]{Fore.RESET} i dont know what happend but it failed")
            try:
                webhooks = []
                with open("webhook.txt", "r") as f:
                    unconverted_webhooks = f.readlines()
                for hook in unconverted_webhooks:
                    webhooks.append(hook.strip())
                for hook in webhooks:
                    if hook.split(":")[0] == "custom_announce":
                        async with session.post("https://announcements-api.herokuapp.com/api/v1/announce", json={"name": target_username}, headers={"Authorization": hook.split(":")[1].strip()}) as r:
                            if r.status_code == 204:
                                logging.info(f"{Fore.WHITE}[{Fore.GREEN}success{Fore.WHITE}]{Fore.RESET} sent custom announcement of snipe!")
                            else:
                                logging.info(r.status, f"{Fore.RED}Failed to send custom announcement!{Fore.RESET}")
                    else:
                        async with session.post(hook, json={"embeds": [{"title": "New Snipe 🎉", "description": f"Sniped `{target_username}` with [MCsniperPY](https://github.com/Kqzz/MCsniperPY)!", "color": 65395}]}) as r:
                            if r.status == 200 or r.status == 204:
                                logging.info(f"{Fore.WHITE}[{Fore.GREEN}success{Fore.WHITE}]{Fore.RESET} sent webhook of snipe!")
                            else:
                                logging.info(r.status)
                                logging.info(await r.json())
            except FileNotFoundError:
                pass


def gather_info():
    block_snipe = menu(options=["Snipe name", "Block Name"])
    target_username = custom_input(f"What name you would you like to {['snipe', 'block'][block_snipe]}: ")
    return block_snipe, target_username


def load_accounts_file():
    accounts = []
    if not path.exists("accounts.txt"):
        print(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}]{Fore.RESET} accounts.txt not found | creating one")
        open('accounts.txt', 'w+')
        input("Press any key to reload accounts. ")
        load_accounts_file()
    else:
        accounts = open('accounts.txt').readlines()
        if len(accounts) == 0:
            print(f"Accounts not found in accounts.txt file please add accounts with format (email:pass) or (email:pass:q1:q2:q3)")
            input("Press any key to reload accounts.")
            load_accounts_file()

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
        self.setup_time = self.drop_time - timedelta(seconds=50)
        self.setup = False
        self.ran = False
        self.settings_json = json.loads(open("settings.json", "r").read())
        if self.settings_json["custom_delay"]:
            if self.snipe_delay == "not specified":
                self.drop_time = self.drop_time - timedelta(milliseconds=int(custom_input("Custom delay in ms: ")))
            else:
                self.drop_time = self.drop_time - timedelta(milliseconds=self.snipe_delay)
        else:
            if self.block_snipe == 0:
                self.drop_time = self.drop_time - timedelta(milliseconds=900)
            elif self.block_snipe == 1:
                self.drop_time = self.drop_time - timedelta(milliseconds=170)

    def run(self):
        loop = asyncio.get_event_loop()
        while True:
            now = datetime.utcnow()
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
                        asyncio.get_event_loop().run_until_complete(self.webhook_skin_file(acc))
                rq_sec = self.num_reqs * len(accounts) / elapsed_time
                times.append(rq_sec)
                logging.info(f"{Fore.GREEN}{str(sum(times))[0:13]}{Fore.CYAN} rqs/sec (ESTIMATE) {Fore.WHITE}|{Fore.CYAN} Took {Fore.WHITE}{str(elapsed_time)[0:8]}{Fore.CYAN} seconds{Fore.RESET} | {self.num_reqs * len(accounts)} requests")
                if len(sys.argv) < 3:
                    custom_input("press enter to quit: ")
                quit()
            elif now >= self.setup_time and not self.setup:
                loop.run_until_complete(self.run_auth())
                for acc in accounts:
                    if acc.failed_auth:
                        logging.info(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}] Removing account: {acc.email} | auth failed")
                        accounts.remove(acc)
                if len(accounts) == 0:
                    logging.info(f"{Fore.WHITE}[{Fore.RED}ERROR{Fore.WHITE}] you have 0 accounts available to snipe on! | quitting program...")
                    quit()
                custom_info("setup complete")
                self.setup = True
            if self.settings_json["async_freeze"]:
                print(self.drop_time - now)
            time.sleep(.00001)

    async def webhook_skin_file(self, acc):
        await acc.webhook_skin_write_file()

    async def send_requests(self):
        async with aiohttp.ClientSession() as session:
            if self.block_snipe == 0:
                self.num_reqs = 20
                self.coros = [
                    acc.snipe_req(session, self.target_username) for acc in self.accounts for _ in range(self.num_reqs)
                ]
            elif self.block_snipe == 1:
                self.num_reqs = 3
                self.coros = [
                    acc.block_req(session, self.target_username) for acc in self.accounts for _ in range(self.num_reqs)
                ]
            await asyncio.wait(self.coros)

    async def run_auth(self):
        async with aiohttp.ClientSession() as session:
            coros = [
                acc.authenticate(session) for acc in self.accounts
            ]
            await asyncio.wait(coros)


print_title()
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
    block_snipe, target_username = gather_info()
    snipe_delay = "not specified"
session = session(target_username, accounts, block_snipe, snipe_delay)
session.run()

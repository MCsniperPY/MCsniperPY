# This code is written by Kqzz on github (github.com/kqzz) and CANNOT be distributed in closed source versions unless specifically given permission.
# If you fork this repo or use the code please join my discord and share your project. Discord: https://discord.gg/jZm4qNF

from datetime import datetime, timedelta
from fake_useragent import UserAgent
from colorama import init, Fore
from time import sleep, time
import threading
# import requests
import asyncio
import aiohttp
import json
import os

# My file imports
from src.util import print_title, ask_option, custom_input, custom_info
from src.get_accs import get_accs_from_txt
from src.sniper_timing import timeSnipe
from src.ask_yes_no import ask_yes_no
from src.sniper_auth import Account


init()
# pre run variables
setup_x_seconds_before = timedelta(seconds=54)
auth_threads = []
threads = []
accounts = []
ua = UserAgent()
not_over = True
setup_snipe = False
sniped = False


print_title()

# loading the accounts
try:
    full_path = os.path.realpath(__file__)
    full_path = os.path.dirname(full_path)
    config_path = os.path.join(full_path, "config.json")
    config = json.load(open(config_path))
except FileNotFoundError:
    accounts_path = os.path.join(full_path, "accounts.txt")
    config = get_accs_from_txt()

for i in config:
    acc = Account(i["email"], i["password"], i["questions"])
    accounts.append(acc)

block_snipe = ask_option(["Block name", "Snipe name", "Run authentication then block name (runs automatically before snipe)", "run authentication then snipe name (runs automatically before snipe)"])

block_snipe_words = ["block", "snipe"]

if block_snipe == 0:
    custom_info("blocking name")
elif block_snipe == 1:
    custom_info("sniping name")
elif block_snipe == 2:
    for acc in accounts:
        t = threading.Thread(target=acc.authenticate)
        t.start()
        auth_threads.append(t)
        sleep(.5)
    for thread in auth_threads:
        thread.join()
    block_snipe = 0
elif block_snipe == 3:
    for acc in accounts:
        t = threading.Thread(target=acc.authenticate)
        t.start()
        auth_threads.append(t)
        sleep(.05)
    for thread in auth_threads:
        thread.join()
    block_snipe = 1

# inputs | Good
target_username = custom_input(f'What name would you like to {block_snipe_words[block_snipe]}? ')
num_reqs = int(custom_input("How many requests should be sent per account? "))
custom_info(f"You will be {block_snipe_words[block_snipe].rstrip('e')}ing a name with {num_reqs} %s per account" % ("request" if num_reqs == 1 else "requests"))
total_reqs = len(accounts) * num_reqs
custom_info(f"This means you will be sending {len(accounts) * num_reqs} requests")
logging_y_n = ask_yes_no("Would you like to log all outputs")
latency = timedelta(milliseconds=int(custom_input("How many ms early should requests start sending? ")))

snipe_time = timeSnipe(target_username, block_snipe)


async def send_requests():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[account.send_request(block_snipe, target_username, logging_y_n, session) for account in accounts for _ in range(num_reqs)])
        # for acc in accounts:
        #     for _ in range(num_reqs):
        #         t = threading.Thread(target=acc.send_request, args=[block_snipe, target_username, logging_y_n, session])
        #         t.start()
        #         threads.append(t)
        #         sleep(.01)


while not_over:
    now = datetime.utcnow()
    if now >= snipe_time - setup_x_seconds_before and not setup_snipe:
        for acc in accounts:
            t = threading.Thread(target=acc.authenticate)
            t.start()
            auth_threads.append(t)
            sleep(.05)
        for thread in auth_threads:
            thread.join()
        for acc in accounts:
            if acc.failed_auth:
                custom_info(Fore.RED + "Removed %s from accounts because auth failed." % acc.email + Fore.RESET)
                accounts.remove(acc)
        custom_info('pre-snipe setup complete')
        setup_snipe = True
        loop = asyncio.get_event_loop()
    elif now >= snipe_time - latency and not sniped:
        start = time()
        custom_info("starting requests for all accounts")
        loop.run_until_complete(send_requests())
        custom_input("All requests have been sent. press enter to close the program: ")
        not_over = False
        sniped = True
    sleep(.001)

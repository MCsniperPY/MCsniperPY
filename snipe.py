# This code is written by Kqzz on github (github.com/kqzz) and CANNOT be distributed in closed source versions unless specifically given permission.
# If you fork this repo or use the code please join my discord and share your project. Discord: https://discord.gg/jZm4qNF

from datetime import datetime, timedelta
from fake_useragent import UserAgent
from colorama import init, Fore
from time import sleep, time
import threading
import requests
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


# snipes based on the global target username. need to change the auth headers tho
# def snipe(config):
#     start = time()
#     if block_snipe == 0:
#         r = requests.put(f"https://api.mojang.com/user/profile/agent/minecraft/name/{target_username}", headers=config['auth'])
#     elif block_snipe == 1:
#         r = requests.post(f"https://api.mojang.com/user/profile/{config['uuid']}/name", headers=config["auth"], json={"name": target_username, "password": config["password"]})

#     if r.status_code == 404 or r.status_code == 400:
#         print(f"{Fore.RED} [ERROR] | Failed to snipe name | {r.status_code}", str(time() - start)[0:10], "|", datetime.now())
#     elif r.status_code == 204 or r.status_code == 200:
#         print(f"{Fore.GREEN} [SUCESS] | Sniped {target_username} onto {config['email']} | {r.status_code}", str(time() - start)[0:10], "|", datetime.now())
#     elif r.status_code == 401:
#         print(f"{Fore.RED} [ERROR] | REQUEST NOT AUTHENTICATED OR RATELIMIT | {r.status_code}", str(time() - start)[0:10], "|", datetime.now())
#     else:
#         print(f"{Fore.RED} [ERROR] | IDK | {r.status_code}", str(time() - start)[0:10], "|", datetime.now())


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

block_snipe = ask_option(["Block name", "Snipe name", "Run authentication then block name (runs automatically before snipe)", "Run authentication then snipe name (runs automatically before snipe)"])

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
custom_info(f"This means you will be sending {len(accounts) * num_reqs} requests")
logging_y_n = ask_yes_no("Would you like to log all outputs")
latency = timedelta(milliseconds=int(custom_input("How many ms early should requests start sending? ")))

snipe_time = timeSnipe(target_username, block_snipe)


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
        custom_info('pre-snipe setup complete')
        setup_snipe = True
    elif now >= snipe_time - latency and not sniped:
        print(datetime.now())
        for acc in accounts:
            for _ in range(num_reqs):
                t = threading.Thread(target=acc.send_request, args=[block_snipe, target_username, logging_y_n])
                t.start()
                threads.append(t)
                sleep(.01)

        not_over = False
        sniped = True
        # for thread in threads:
        #     thread.join()
    sleep(.001)

sleep(3)
custom_input("press enter to close the program: ")
# I really don't want to put that in but since so many people run by double clicking it i have to :(

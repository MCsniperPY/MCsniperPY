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
from src.sniper_auth import full_auth, no_questions_full_auth
from src.get_accs import get_accs_from_txt
from src.sniper_timing import timeSnipe
from src.ask_yes_no import ask_yes_no


init()
setup_x_seconds_before = timedelta(seconds=50)
auth_threads = []
threads = []
ua = UserAgent()
not_over = True
latency = timedelta(milliseconds=80)
setup_snipe = False
sniped = False


def snipe(config):
    start = time()
    if block_snipe == 0:
        r = requests.put(f"https://api.mojang.com/user/profile/agent/minecraft/name/{target_username}", headers=auth)
    elif block_snipe == 1:
        r = requests.post(f"https://api.mojang.com/user/profile/{config['uuid']}/name", headers=config["auth"], json={"name": target_username, "password": config["password"]})
    if r.status_code == 404 or r.status_code == 400:
        print(f"{Fore.RED} [ERROR] | Failed to snipe name | {r.status_code}", time() - start, "|", datetime.now())
    elif r.status_code == 204 or r.status_code == 200:
        print(f"{Fore.GREEN} [SUCESS] | Sniped {target_username} onto {config['email']} | {r.status_code}", time() - start, "|", datetime.now())
    elif r.status_code == 401:
        print(f"{Fore.RED} [ERROR] | REQUEST NOT AUTHENTICATED OR RATELIMIT | {r.status_code}", time() - start, "|", datetime.now())


print_title()

try:
    full_path = os.path.realpath(__file__)
    full_path = os.path.dirname(full_path)
    config_path = os.path.join(full_path, "config.json")
    config = json.load(open(config_path))
except FileNotFoundError:
    accounts_path = os.path.join(full_path, "accounts.txt")
    config = get_accs_from_txt()


# checking the json file for missing fields
block_snipe = ask_option(["Block name", "Snipe name"])
if block_snipe == 0:
    custom_info("blocking name")
elif block_snipe == 1:
    custom_info("sniping name")
target_username = custom_input('What name would you like to snipe? ')
added_latency = int(custom_input("How many ms early should requests start sending? "))
security_questions_yes_no = ask_yes_no(f"{Fore.BLUE}[input]{Fore.RESET} Does your account have security questions")


if security_questions_yes_no:
    custom_info('starting auth for accounts with security questions')
    i = 0
    for account in config:
        config[i]['uuid'], config[i]['auth'] = full_auth(account)
        custom_info("part of uuid: " + config[i]["uuid"][0:15])
        i += 1
if not security_questions_yes_no:
    custom_info('starting auth for accounts without security questions')
    i = 0
    for account in config:
        config[i]['uuid'], config[i]['auth'] = no_questions_full_auth(account)
        custom_info("part of uuid: " + config[i]["uuid"][0:15])
        i += 1
snipe_time = timeSnipe(target_username)

while not_over:
    now = datetime.utcnow()
    if now >= snipe_time - setup_x_seconds_before and not setup_snipe:
        if security_questions_yes_no:
            i = 0
            for account in config:
                config[i]['uuid'], auth = full_auth(account)
                i += 1
        if not security_questions_yes_no:
            i = 0
            for account in config:
                config[i]['uuid'], auth = no_questions_full_auth(account)
                i += 1
        setup_snipe = True
    elif now >= snipe_time - latency and not sniped:
        custom_info("sniping now")
        for i in range(len(config)):
            for _ in range(20):
                t = threading.Thread(target=snipe, args=[config[i]])
                t.start()
                threads.append(t)
                sleep(.015)

        for thread in threads:
            thread.join()
        not_over = False
        sniped = True
    sleep(.001)

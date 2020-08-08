# This code is written by Kqzz on github (github.com/kqzz) and CANNOT be distributed in closed source versions unless specifically given permission.
# If you fork this repo or use the code please join my discord and share your project. Discord: https://discord.gg/jZm4qNF

import requests
import os
import json
from time import sleep, time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime, timedelta
from colorama import init, Fore
import threading

# My file imports
from src.sniper_timing import timeSnipe
from src.sniper_auth import full_auth, no_questions_full_auth
from src.ask_yes_no import ask_yes_no
from src.get_accs import get_accs_from_txt
from src.util import get_latency, print_title, ask_option, custom_input, custom_info


init()
setup_x_seconds_before = timedelta(seconds=50)
threads = []
ua = UserAgent()
not_over = True
latency = timedelta(milliseconds=80)
setup_snipe = False
sniped = False


def snipe(config):
    start = time()
    r = requests.post(f"https://api.mojang.com/user/profile/{config['uuid']}/name", headers=auth, json={"name": target_username, "password": config["password"]})
    if r.status_code == 404 or 400:
        print(f"{Fore.RED} [ERROR] | Failed to snipe name | {r.status_code}", time() - start, "|", datetime.now())
    elif str(r.status_code)[0] == '2':
        print(f"{Fore.GREEN} [SUCESS] | Sniped {target_username} onto {config['email']} | {r.status_code}", time() - start, "|", datetime.now())
        can_post_to_webhook = ask_yes_no('May we post your successful snipe to our discord server')
        if can_post_to_webhook:
            page = requests.get(f'https://namemc.com/name/{target_username}')
            soup = BeautifulSoup(page.content, 'html.parser')
            status_bar = soup.find(id="status-bar")
            info = status_bar.find_all("div", class_="col-sm-6 my-1")
            searches_per_month = info[1].text.split("\n")[2].split(" ")[0]
            data = {}
            data["content"] = f"Sucessfully sniped `{target_username}` which has `{searches_per_month}` searches per month."
            data["username"] = "Sniper"
            result = requests.post("https://discordapp.com/api/webhooks/739595348917354545/5RsrTA0McxDXqg7gtfF6bqaWbtqVuuJf86bUyIE05pDSqV2_uzH5DwG12LUuhALU3hAK", json=data, headers={"Content-Type": "application/json"})
            if result.status_code == 200:
                print('successfully posted to webhook. Thanks for using my sniper.')
    elif r.status_code == 401:
        print(f"{Fore.RED} [ERROR] | REQUEST NOT AUTHENTICATED | {r.status_code}", time() - start, "|", datetime.now())


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
        config[i]['uuid'], config[i]['auth'] = no_questions_full_auth(config)
        print(config)
        i += 1
snipe_time = timeSnipe(target_username)

while not_over:
    now = datetime.utcnow()
    if now >= snipe_time - setup_x_seconds_before and not setup_snipe:
        if security_questions_yes_no:
            i = 0
            for account in config:
                config[i]['uuid'], auth = full_auth(account)
                print(config)
                i += 1
        if not security_questions_yes_no:
            i = 0
            for account in config:
                config[i]['uuid'], auth = no_questions_full_auth(config)
                print(config)
                i += 1
        latency = get_latency(added_latency)
        setup_snipe = True
    elif now >= snipe_time - latency and not sniped:
        custom_info("sniping now")
        for i in range(len(config)):
            for _ in range(19):
                t = threading.Thread(target=snipe, args=[config[i]])
                t.start()
                threads.append(t)
                sleep(.015)

        for thread in threads:
            thread.join()
        not_over = False
        sniped = True
    sleep(.001)

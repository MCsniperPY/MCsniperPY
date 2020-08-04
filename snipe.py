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


init()
thirty_sec = timedelta(seconds=30)
threads = []
ua = UserAgent()
# session = AsyncSession(n=20)
not_over = True
latency = timedelta(milliseconds=80)
setup_snipe = False
sniped = False


def snipe():
    # current_agent = ua.random
    # auth["User-Agent"] = current_agent
    # auth["X-Forwarded-For"] = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    # print(Fore.GREEN, "sending request |", datetime.now())
    start = time()
    r = requests.post(f"https://api.mojang.com/user/profile/{uuid}/name", headers=auth, json={"name": config["target"], "password": config["password"]})
    if r.status_code == 404 or 400:
        print(f"{Fore.RED} [ERROR] | Failed to snipe name | {r.status_code}", time() - start, "|", datetime.now())
    elif str(r.status_code)[0] == '2':
        print(f"{Fore.GREEN} [SUCESS] | Sniped {config['target']} onto {config['email']} | {r.status_code}", time() - start, "|", datetime.now())
        can_post_to_webhook = ask_yes_no('May we post your successful snipe to our discord server')
        if can_post_to_webhook:
            page = requests.get(f'https://namemc.com/name/{config["target"]}')
            soup = BeautifulSoup(page.content, 'html.parser')
            status_bar = soup.find(id="status-bar")
            info = status_bar.find_all("div", class_="col-sm-6 my-1")
            searches_per_month = info[1].text.split("\n")[2].split(" ")[0]
            data = {}
            data["content"] = f"Sucessfully sniped `{config['target']}` which has `{searches_per_month}` searches per month."
            data["username"] = "Sniper"
            result = requests.post("https://discordapp.com/api/webhooks/739595348917354545/5RsrTA0McxDXqg7gtfF6bqaWbtqVuuJf86bUyIE05pDSqV2_uzH5DwG12LUuhALU3hAK", json=data, headers={"Content-Type": "application/json"})
            if result.status_code == 200:
                print('successfully posted to webhook. Thanks for using my sniper.')
    elif r.status_code == 401:
        print(f"{Fore.RED} [ERROR] | REQUEST NOT AUTHENTICATED | {r.status_code}", time() - start, "|", datetime.now())


#                          _               _   _                          _      
#   _ __ _   _ _ __  _ __ (_)_ __   __ _  | |_| |__   ___    ___ ___   __| | ___ 
#  | '__| | | | '_ \| '_ \| | '_ \ / _` | | __| '_ \ / _ \  / __/ _ \ / _` |/ _ \
#  | |  | |_| | | | | | | | | | | | (_| | | |_| | | |  __/ | (_| (_) | (_| |  __/
#  |_|   \__,_|_| |_|_| |_|_|_| |_|\__, |  \__|_| |_|\___|  \___\___/ \__,_|\___|
#                                  |___/                                         

print(f"""

{Fore.RESET}███╗   ███╗ ██████╗███████╗███╗   ██╗██╗██████╗ ███████╗██████╗ {Fore.BLUE}██████╗ ██╗   ██╗
{Fore.RESET}████╗ ████║██╔════╝██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗{Fore.BLUE}██╔══██╗╚██╗ ██╔╝
{Fore.RESET}██╔████╔██║██║     ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝{Fore.BLUE}██████╔╝ ╚████╔╝ 
{Fore.RESET}██║╚██╔╝██║██║     ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗{Fore.BLUE}██╔═══╝   ╚██╔╝  
{Fore.RESET}██║ ╚═╝ ██║╚██████╗███████║██║ ╚████║██║██║     ███████╗██║  ██║{Fore.BLUE}██║        ██║   
{Fore.RESET}╚═╝     ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝{Fore.BLUE}╚═╝        ╚═╝
{Fore.GREEN}Developed by @Kqzz#0001 on Discord {Fore.BLUE}| Discord server: https://discord.gg/jZm4qNF |{Fore.GREEN} THIS SNIPER IS 100% FREE ON GITHUB
""", Fore.RESET)
full_path = os.path.realpath(__file__)
full_path = os.path.dirname(full_path)
config_path = os.path.join(full_path, "config.json")

config = json.load(open(config_path))


# checking the json file for missing fields
config["target"] = input('What name would you like to snipe? ')
if config['email'] == '':
    print("missing email")
    quit()
if config["password"] == '':
    print('Missing Password!')
    quit()


security_questions_yes_no = ask_yes_no("Does your account have security questions")
if security_questions_yes_no:
    uuid = full_auth(config)
if not security_questions_yes_no:
    no_questions_full_auth(config)
snipe_time = timeSnipe(config)

while not_over:
    now = datetime.utcnow()
    if now >= snipe_time - thirty_sec and not setup_snipe:
        if security_questions_yes_no:
            uuid = full_auth(config)
        if not security_questions_yes_no:
            no_questions_full_auth(config)
        start_latency = time()
        requests.post(f"https://api.mojang.com/user/profile/{uuid}/name")
        latency = time() - start_latency
        latency = latency * 1000 * 3 + 2_100
        print("sniping", latency, "ms before drop time.")
        latency = timedelta(milliseconds=latency)
        setup_snipe = True
    elif now >= snipe_time - latency and not sniped:
        print("Sniping now")
        for _ in range(19):
            t = threading.Thread(target=snipe)
            t.start()
            threads.append(t)
            sleep(.015)

        for thread in threads:
            thread.join()
        not_over = False
        sniped = True

# This code is written by Kqzz on github (github.com/kqzz) and CANNOT be distributed in closed source versions.
# If you fork this repo or use the code please join my discord and share your project. Discord: https://discord.gg/jZm4qNF

from ping3 import ping
import requests
import os
import json
from time import sleep, time
from bs4 import BeautifulSoup
from dateutil import tz
from fake_useragent import UserAgent
from datetime import datetime, timedelta
# from requests_threads import AsyncSession
from colorama import init, Fore
import threading
import random


init()
thirty_sec = timedelta(seconds=30)
threads = []
ua = UserAgent()
# session = AsyncSession(n=20)
not_over = True
latency = timedelta(milliseconds=80)
setup_snipe = False
sniped = False

print("""
___  ________             _                ________   __
|  \/  /  __ \           (_)               | ___ \ \ / /
| .  . | /  \/  ___ _ __  _ _ __   ___ _ __| |_/ /\ V / 
| |\/| | |     / __| '_ \| | '_ \ / _ \ '__|  __/  \ /  
| |  | | \__/\ \__ \ | | | | |_) |  __/ |  | |     | |  
\_|  |_/\____/ |___/_| |_|_| .__/ \___|_|  \_|     \_/  
                           | |                          
                           |_|                          
 """)



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


def timeSnipe(config):
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    now = datetime.strptime(now, '%Y-%m-%dT%H:%M:%S')

    try:
        namemc_url = f"https://namemc.com/search?q={config['target']}"
        page = requests.get(namemc_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        snipe_time = soup.find("time", {"id": "availability-time"}).attrs["datetime"]
        snipe_time = datetime.strptime(snipe_time, '%Y-%m-%dT%H:%M:%S.000Z')
    except AttributeError:
        status_bar = soup.find(id="status-bar")
        info = status_bar.find_all("div", class_="col-sm-6 my-1")
        status = info[0].text.split("\n")[2]
        print(f"\"{config['target']}\" is {status}. The sniper cannot claim names that are {status} so go claim it fast through https://my.minecraft.net if possible.")
        quit()

    wait_time = snipe_time - now
    wait_time = wait_time.seconds
    print(f"Sniping \"{config['target']}\" in", wait_time, f"seconds | Sniping at {snipe_time} (utc)")
    return snipe_time


def authenticate(email, password):
    authenticate_json = {"agent": {"name": "Minecraft", "version": 1}, "username": email, "password": password}
    headers = {"User-Agent": ua.random, "Content-Type": "application/json"}
    r = requests.post("https://authserver.mojang.com/authenticate", json=authenticate_json, headers=headers)
    config["username"] = r.json()["selectedProfile"]["name"]
    return r.json()["accessToken"], r.json()["selectedProfile"]["name"], r.json()["selectedProfile"]["id"]


def get_questions(bearer):
    global auth
    auth = {"Authorization": "Bearer: " + config["bearer"]}
    questions = requests.get("https://api.mojang.com/user/security/challenges", headers=auth)
    questions = questions.json()
    try:
        if questions["errorMessage"] == "The request requires user authentication":
            print("Bearer didn't work...")
    except TypeError:
        return questions

def validate(token):
    r = requests.post("https://authserver.mojang.com/validate", json={"accessToken": token}, headers={"User-Agent": ua.random, "Content-Type": "application/json"})
    if r.status_code != 204:
        print(Fore.RED, "Failed to authenticate", Fore.RESET)
def acc_setup(config, questions, uuid):
    answers = []
    if len(questions) == 0:
        return

    for i in range(3):
        answers.append({"id": questions[i]["answer"]["id"], "answer": config["questions"][i]})
    post_answers = requests.post("https://api.mojang.com/user/security/location", json=answers, headers=auth)
    if post_answers.status_code != 204:
        print(f"{Fore.RED} Failed: {post_answers.text} {Fore.RESET}")
    else:
        print(f"{Fore.GREEN} credentials for {config['username']} verified {Fore.RESET} ")


def full_auth():
    global uuid
    config["bearer"], config["username"], uuid = authenticate(config["email"], config["password"])
    qs = get_questions(config["bearer"])
    acc_setup(config, qs, uuid)
    validate(config["bearer"])


def snipe():
    # current_agent = ua.random
    # auth["User-Agent"] = current_agent
    # auth["X-Forwarded-For"] = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    # print(Fore.GREEN, "sending request |", datetime.now())
    start = time()
    r = requests.post(f"https://api.mojang.com/user/profile/{uuid}/name", headers=auth, json={"name": config["target"], "password": config["password"]})
    if r.status_code == 404 or 400:
        print(f"{Fore.RED} [ERROR] | Failed to snipe name | {r.status_code}", time() - start, "|", datetime.now())
    elif r.status_code == 201:
        print(f"{Fore.GREEN} [SUCESS] | Sniped {config['target']} onto {config['email']} | {r.status_code}", time() - start, "|", datetime.now())
    elif r.status_code == 401:
        print(f"{Fore.RED} [ERROR] | REQUEST NOT AUTHENTICATED | {r.status_code}", time() - start, "|", datetime.now())

full_auth()
snipe_time = timeSnipe(config)

while not_over:
    now = datetime.utcnow()
    if now >= snipe_time - thirty_sec and not setup_snipe:
        full_auth()
        latency = ping("api.mojang.com")
        latency = latency * 1000 * 3 + 1_300
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

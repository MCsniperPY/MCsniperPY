import requests
from colorama import Fore
from fake_useragent import UserAgent
ua = UserAgent()


def authenticate(config):
    authenticate_json = {"agent": {"name": "Minecraft", "version": 1}, "username": config['email'], "password": config['password']}
    headers = {"User-Agent": ua.random, "Content-Type": "application/json"}
    r = requests.post("https://authserver.mojang.com/authenticate", json=authenticate_json, headers=headers)
    config["username"] = r.json()["selectedProfile"]["name"]
    return r.json()["accessToken"], r.json()["selectedProfile"]["name"], r.json()["selectedProfile"]["id"]


def get_questions(config):
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


def no_questions_full_auth(config):
    config["bearer"], config["username"], uuid = authenticate(config)
    get_questions(config)
    validate(config["bearer"])
    return uuid


def full_auth(config):
    global uuid
    config["bearer"], config["username"], uuid = authenticate(config)
    qs = get_questions(config)
    acc_setup(config, qs, uuid)
    validate(config["bearer"])
    return uuid

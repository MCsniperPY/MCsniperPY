import requests
from bs4 import BeautifulSoup
from datetime import datetime
from src.util import custom_info

def timeSnipe(target):
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    now = datetime.strptime(now, '%Y-%m-%dT%H:%M:%S')

    try:
        namemc_url = f"https://namemc.com/search?q={target}"
        page = requests.get(namemc_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        snipe_time = soup.find("time", {"id": "availability-time"}).attrs["datetime"]
        snipe_time = datetime.strptime(snipe_time, '%Y-%m-%dT%H:%M:%S.000Z')
    except AttributeError:
        status_bar = soup.find(id="status-bar")
        info = status_bar.find_all("div", class_="col-sm-6 my-1")
        status = info[0].text.split("\n")[2]
        print(f"\"{target}\" is {status}. The sniper cannot claim names that are {status} so go claim it fast through https://my.minecraft.net if possible.")
        quit()

    wait_time = snipe_time - now
    wait_time = wait_time.seconds
    custom_info(f"Sniping \"{target}\" in {wait_time} seconds | Sniping at {snipe_time} (utc)")
    return snipe_time

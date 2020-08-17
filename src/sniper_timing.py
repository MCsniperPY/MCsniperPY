import requests
from bs4 import BeautifulSoup
from datetime import datetime
from src.util import custom_info, custom_input


def timeSnipe(target, block_snipe):
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    now = datetime.strptime(now, '%Y-%m-%dT%H:%M:%S')
    block_snipe_words = ["block", "snipe"]

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
        if status.lower().rstrip('*') == 'available':
            snipe_time = custom_input("At what time will this name be able to be turboed (month/day/yr, 24hrtime_hour:minute:second) (UTC)\nexample: 03/06/2020 01:06:45\n» ")
            snipe_time = datetime.strptime(snipe_time.strip(), "%m/%d/%Y %H:%M:%S")
            wait_time = snipe_time - now
            wait_time = wait_time.seconds / 60
            custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in {wait_time} minutes | Sniping at {snipe_time} (utc)")
            return snipe_time
        print(f"\"{target}\" is {status}. The sniper cannot claim names that are {status} so go claim it fast through https://my.minecraft.net if possible.")
        quit()

    wait_time = snipe_time - now
    wait_time = wait_time.seconds
    custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in {wait_time} seconds | Sniping at {snipe_time} (utc)")
    return snipe_time

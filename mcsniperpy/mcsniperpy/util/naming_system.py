from datetime import datetime
import sys
import requests
from bs4 import BeautifulSoup
from . import logs_manager as log


def namemc(name):
    r = requests.get(f"https://namemc.com/search?q={name}")

    try:
        soup = BeautifulSoup(r.content, 'html.parser')
        snipe_time = soup.find("time", {"id": "availability-time"}).attrs["datetime"]
        snipe_time = datetime.strptime(snipe_time, '%Y-%m-%dT%H:%M:%S.000Z')
        return snipe_time.timestamp()
    except Exception:
        log.error(f"Couldn't get droptime from namemc. Maybe the name isn't dropping?")
        sys.exit(0)

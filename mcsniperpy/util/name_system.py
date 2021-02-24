from datetime import datetime
import sys
import requests
from bs4 import BeautifulSoup
from .logs_manager import Logger as log, Color as color
from .request_manager import RequestManager


async def namemc_timing(name):
    r = requests.get(f"https://namemc.com/search?q={name}")

    try:
        soup = BeautifulSoup(r.content, 'html.parser')
        snipe_time = soup.find("time", {"id": "availability-time"}).attrs["datetime"]
        snipe_time = datetime.strptime(snipe_time, '%Y-%m-%dT%H:%M:%S.000Z')
        return snipe_time.timestamp()
    except Exception as e:  # Need to find all the cases why this is triggered
        log.error(e)
        log.error(f"Couldn't get droptime from namemc. Maybe the name isn't dropping?")
        sys.exit(0)


async def api_timing(username: str, session: RequestManager) -> int:  # Returns a unix timestamp
    resp, _, resp_json = await session.get(f"https://api.kqzz.me/api/namemc/droptime/{username}")
    if resp_json.get("error", None) is not None:
        return resp_json['droptime']
    else:
        log.error(f"failed to parse droptime for {color.l_cyan}{username}")
        log.error(f"{resp_json['error']}")

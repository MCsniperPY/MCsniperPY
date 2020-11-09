from utils import *
import time
from datetime import datetime, timezone

try:
    import aiohttp
    from colorama import Fore, init
    from bs4 import BeautifulSoup
except ImportError:
    print("You are missing the required modules | Please refer to the usage on how to install")
    quit()


async def mojang_timing(target, block_snipe):
    block_snipe_words = ["snipe", "block"]
    async with aiohttp.ClientSession() as session:
        old_name_time = int(time.time() - 3456000)
        async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{target}?at={old_name_time}") as r:
            try:
                resp_json = await r.json()
            except Exception:
                print(f"{Fore.WHITE}[{Fore.RED}error{Fore.WHITE}]{Fore.RESET} Cannot snipe name \"{target}\" | It is either blocked, invalid, or has had no previous owners.")
                time.sleep(2)
                quit()
            async with session.get(f"https://api.mojang.com/user/profiles/{resp_json['id']}/names") as r:
                old_owner = await r.json()
                previous_names = len(old_owner)
                snipe_time = (old_owner[previous_names - 1]["changedToAt"] / 1000) + 3196800
                if snipe_time > time.time() + 172800:
                    try:
                        snipe_time = (old_owner[previous_names - 2]["changedToAt"] / 1000) + 3196800
                    except KeyError:
                        resp_error(f"\"{target}\" is unavailable | The sniper cannot claim unavailable names")
                if snipe_time < time.time():
                    print(f"{Fore.WHITE}[{Fore.RED}error{Fore.WHITE}]{Fore.RESET} \"{target}\" is available | The sniper cannot claim available names with this timing system")
                    custom_info("replace \"timing_system:api\" with \"timing_system:namemc\" in config.txt for turboing a name")
                    time.sleep(2)
                    quit()
                wait_time = snipe_time - time.time()
                if wait_time >= 60 and wait_time <= 3600:
                    custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in ~{round(wait_time / 60, 1)} minutes | {block_snipe_words[block_snipe].rstrip('e')}ing at {datetime.fromtimestamp(snipe_time)} (utc)")
                elif wait_time >= 3600:
                    custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in ~{round(wait_time / 3600, 2)} hours | {block_snipe_words[block_snipe].rstrip('e')}ing at {datetime.fromtimestamp(snipe_time)} (utc)")
                else:
                    custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in ~{round(wait_time)} seconds | {block_snipe_words[block_snipe].rstrip('e')}ing at {datetime.fromtimestamp(snipe_time)} (utc)")
                return snipe_time


async def namemc_timing(target, block_snipe):
    now = datetime.utcnow()
    block_snipe_words = ["snipe", "block"]
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"https://namemc.com/search?q={target}") as page:
                # page = requests.get(namemc_url)
                soup = BeautifulSoup(await page.text(), 'html.parser')
                snipe_time = soup.find("time", {"id": "availability-time"}).attrs["datetime"]
                snipe_time = datetime.strptime(snipe_time, '%Y-%m-%dT%H:%M:%S.000Z')
        except AttributeError:
            status_bar = soup.find(id="status-bar")
            info = status_bar.find_all("div", class_="col-sm-6 my-1")
            status = info[0].text.split("\n")[2]
            if status.lower().rstrip('*') == 'available':
                custom_info(f"\"{target}\" is {status}. The sniper can turbo {status} names!")
                snipe_time = custom_input("At what time will this name be able to be turboed (month/day/yr, 24hrtime_hour:minute:second) (UTC)\nexample: 03/06/2020 01:06:45\n» ")
                try:
                    snipe_time = datetime.strptime(snipe_time.strip(), "%m/%d/%Y %H:%M:%S")
                except ValueError:
                    resp_error("invalid time format")
                    raise ValueError
                wait_time = snipe_time - now
                wait_time = wait_time.seconds
                if wait_time >= 60:
                    custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in ~{round(wait_time / 60)} minutes | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
                else:
                    custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in {wait_time} seconds | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
                custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in {wait_time} minutes | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
                return int(snipe_time.replace(tzinfo=timezone.utc).timestamp())
            print(f"\"{target}\" is {status}. The sniper cannot claim names that are {status} so go claim it fast through https://my.minecraft.net if possible.")
            quit()

        wait_time = snipe_time - now
        wait_time = wait_time.seconds
        if wait_time >= 60:
            custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in ~{round(wait_time / 60)} minutes | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
        elif wait_time >= 3600:
            custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in ~{round(wait_time / 3600)} minutes | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
        else:
            custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in {wait_time} seconds | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
        return int(snipe_time.replace(tzinfo=timezone.utc).timestamp())


async def nx_timing(target, block_snipe):
    now = datetime.utcnow()
    block_snipe_words = ["snipe", "block"]
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.nathan.cx/check/{target}") as r:
            resp_json = await r.json()
            if resp_json["status"] == "soon":
                snipe_time = datetime.strptime(resp_json()["drop_time"], "%Y-%m-%dT%H:%M:%S.000Z")
            elif resp_json["status"] == "taken":
                resp_error(f"\"{target}\" is taken already. The sniper cannot claim names that are taken.")
                # time.sleep(2)
                # quit()
            if resp_json["status"] == "":
                custom_info(f"{target} is available now. If you would like to turbo the name see below.")
                snipe_time = custom_input("At what time will this name be able to be turboed (month/day/yr, 24hrtime_hour:minute:second) (UTC)\nexample: 03/06/2020 01:06:45\n» ")
                snipe_time = datetime.strptime(snipe_time.strip(), "%m/%d/%Y %H:%M:%S")
                wait_time = snipe_time - now
                wait_time = wait_time.seconds
                if wait_time >= 60:
                    custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in ~{round(wait_time / 60)} minutes | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
                else:
                    custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in {wait_time} seconds | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
                custom_info(f"{block_snipe_words[block_snipe].rstrip('e')}ing \"{target}\" in {wait_time} minutes | {block_snipe_words[block_snipe].rstrip('e')}ing at {snipe_time} (utc)")
                return snipe_time.timestamp()

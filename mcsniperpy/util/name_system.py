import asyncio
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup

from mcsniperpy.util.logs_manager import Logger as log, Color as color
from mcsniperpy.util.request_manager import RequestManager
from mcsniperpy.util.utils import close


async def namemc_timing(username: str, session: RequestManager) -> float:
    resp, text, _ = await session.get(f"https://namemc.com/search?q={username}")

    if resp.status != 502:
        try:
            soup = BeautifulSoup(text, "html.parser")

            status_bar = soup.find(id="status-bar")
            info = status_bar.find_all("div", class_="col-sm-6 my-1")

            name_status = info[0].text.split("\n")[2].strip("*").lower()
            pretty_username = f"{color.l_cyan}{username}{color.reset}"
            pretty_status = f"{color.yellow if name_status == 'Unavailable' else color.green}{name_status}{color.reset}"

            if name_status == "unavailable":
                log.error(
                    f"failed to parse droptime for {pretty_username} through namemc"
                )
                log.info(
                    f"the username {pretty_username} is {pretty_status} at the moment which is most likely your problem!"
                )
                close(1)
            elif name_status == "available":
                log.info(
                    f"failed to parse droptime for {pretty_username} through namemc"
                )
                log.info(
                    f"the username {pretty_username} is {pretty_status} at the moment!"
                )
                log.info("go claim it without the sniper if possible.")
                close(1)
            elif name_status == "available later":
                snipe_time = soup.find("time", {"id": "availability-time"}).attrs[
                    "datetime"
                ]
                snipe_time = datetime.strptime(snipe_time, "%Y-%m-%dT%H:%M:%S.000Z")
                log.info(f"sniping {pretty_username} @ {snipe_time}")
                return snipe_time.timestamp()
            else:
                log.error(
                    "well this is awkward. You shouldn't be able to get here, but you are."
                )
                log.info(f"the status is {pretty_status}")
                close(1)
        # pylint: disable=broad-except
        except Exception as ex:
            # TODO: Need to find all the cases why this is triggered
            log.error(ex)
            log.error(
                "Couldn't get droptime from namemc. "
                "Maybe the name isn't dropping?"
            )
            close(0)
    else:
        log.error(f"failed to connect to {color.l_blue}namemc.com")
        close(1)

    close(1)
    return 0


async def teun_timing(
    username: str,
    session: RequestManager
) -> int:  # Returns a unix timestamp
    resp, _, resp_json = await session.get(
        f"https://mojang-api.teun.lol/droptime/{username}"
    )
    if resp.status < 300:
        log.info(
            f"sniping {color.cyan}{username}{color.reset} @ {datetime.fromtimestamp(resp_json['UNIX'])}"
        )
        return resp_json["UNIX"]

    log.error(
        f"failed to parse droptime for {color.l_cyan}{username}{color.reset} through teuns's MC API"
    )
    log.error(f"{resp_json['error']} | {resp.status}")

    close(0)
    return 0


async def coolkidmacho_timing(
        username: str,
        session: RequestManager
):
    resp, _, resp_json = await session.get(
        f"http://api.coolkidmacho.com/droptime/{username}"
    )

    if resp.status < 300:
        log.info(
            f"sniping {color.cyan}{username}{color.reset} @ {datetime.fromtimestamp(resp_json['UNIX'])}"
        )
        return resp_json["UNIX"]

    log.error(
        f"failed to parse droptime for {color.l_cyan}{username}{color.reset} through Coolkidmacho's droptime API"
    )
    log.error(f"{resp_json['error']} | {resp.status}")

    close(0)
    return 0


async def api_timing(
    username: str,
    session: RequestManager
) -> int:  # Returns a unix timestamp
    resp, _, resp_json = await session.get(
        f"https://api.kqzz.me/api/namemc/droptime/{username}"
    )
    # pylint: disable=no-else-return
    if resp_json.get("error", None) is None:
        log.info(
            f"sniping {color.cyan}{username}{color.reset} @ {datetime.fromtimestamp(resp_json['droptime'])}"
        )
        return resp_json["droptime"]
    else:
        log.error(
            f"failed to parse droptime for {color.l_cyan}{username}{color.reset} through Kqzz's MC API"
        )
        log.error(f"{resp_json['error']} | {resp.status}")
        close(0)

    close(0)
    return 0


def next_name(
    base_url: str = "https://api.kqzz.me",
    searches: int = 0,
    loop=asyncio.get_event_loop(),
):
    async def do_request():
        async with aiohttp.ClientSession() as session:
            resp = await session.get(
                base_url + "/api/namemc/upcoming?searches=" + str(searches)
            )
            upcoming_names = await resp.json()
        if len(upcoming_names) > 0:
            return upcoming_names[0]["name"]
        return None

    return loop.run_until_complete(do_request())

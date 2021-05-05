import re
from datetime import datetime

from mcsniperpy.util.logs_manager import Color as color
from mcsniperpy.util.logs_manager import Logger as log
from mcsniperpy.util.request_manager import RequestManager


async def announce(
    username: str,
    authorization: str,
    session: RequestManager,
    full_url: str = "https://announcements-api.herokuapp.com/api/v1/announce",
) -> bool:
    headers = {"Authorization": authorization}
    json = {"name": username}
    resp, _, resp_json = await session.post(full_url, json=json, headers=headers)
    if resp.status < 300:
        log.info(f"{color.white}[{color.l_green}success{color.white}]{color.reset}")
        return True

    log.error(f"Failed to announce snipe | {resp.status} | {resp_json}")
    return False


DISCORD_RESP_CODES = {
    200: "ok",
    201: "created",
    204: "ok (no content)",
    304: "not modified",
    400: "bad request",
    401: "unauthorized",
    403: "forbidden",
    404: "not found",
    405: "method not allowed",
    429: "too many requests",
    502: "gateway unavailable",
    500: "server error",
}


async def gen_webhook_desc(desc_format, name, session: RequestManager):
    resp, _, resp_json = await session.get(
        f"https://api.kqzz.me/api/namemc/searches/{name}"
    )

    searches: int = 0

    if resp.status < 300:
        searches = resp_json["searches"]
    else:
        searches = 0

    final_format = desc_format.format(
        name=name, searches=searches, namemcLink=f"https://namemc.com/profile/{name}"
    )

    return final_format


async def webhook_announce(
    webhook_url: str,
    session: RequestManager,
    embed_description: str,
    embed_title: str,
    prename: bool = False,
    embed_color: int = 0x779ABD,
):
    regex = re.compile(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|"
        r"[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    if regex.match(webhook_url):
        action = "prenamed" if prename else "sniped"
        embed_content ={
            "content": None,
            "embeds": [                {
                    "title": embed_title,
                    "description": embed_description,
                    "color": embed_color,
                    "footer": {
                        "text": f"{action.title()} with MCsniperPY",
                        "icon_url": "https://mcsniperpy.com/img/old-logo.png",
                    },
                    "timestamp": datetime.utcnow().strftime(
                        "%Y-%m-%dT%H:%M:%S.000Z"
                    ),
                }
            ],
        }
        resp, _, _ = await session.post(webhook_url, json=embed_content)
        if resp.status < 300:
            log.info(
                f"{color.white}[{color.l_green}success{color.white}]{color.reset} "
                "successfully sent discord webhook!"
            )
            return True

        log.error(
            f"failed to send Discord webhook | {resp.status} | "
            f"{DISCORD_RESP_CODES.get(resp.status, 'unknown')}"
        )

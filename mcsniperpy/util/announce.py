from mcsniperpy.util.request_manager import RequestManager
from mcsniperpy.util.logs_manager import Logger as log
from mcsniperpy.util.logs_manager import Color as color


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
        log.info(f'{color.white}[{color.l_green}success{color.white}]{color.reset}')
        return True

    log.error(f"Failed to announce snipe | {resp.status} | {resp_json}")
    return False


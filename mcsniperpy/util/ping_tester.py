# type: ignore
# ^ that's necessary to prevent a false linting error of some kind
import asyncio
import urllib.parse
from time import perf_counter

import typer
from mcsniperpy.util.logs_manager import Color as color
from mcsniperpy.util.logs_manager import Logger as log


async def check(url: str, iterations: int):
    async def ping():
        try:
            uri = urllib.parse.urlparse(url)
            reader, writer = await asyncio.open_connection(uri.hostname, 443, ssl=False)
            writer.write(
                f"GET {uri.path or '/'} HTTP/1.1\r\nHost:{uri.hostname}\r\n\r\n".encode()
            )

            start = perf_counter()
            await writer.drain()

            _ = await reader.read(100)
            end = perf_counter()
            return round((end - start) * 1000)
        # pylint: disable=invalid-name, broad-except
        except Exception as e:
            log.error("Failed to connect to URL. error code: " + str(e))

    pings = []

    with typer.progressbar(
        range(iterations),
        fill_char="█",
        empty_char=" ",
        color=10,
        show_eta=False,
        bar_template="%(label)s  %(bar)s  %(info)s",
    ) as progress:
        for _ in progress:
            pings.append(await ping())
            await asyncio.sleep(0.01)

    print()
    log.info(f"Host {color.l_cyan}» {color.blue}{urllib.parse.urlparse(url).hostname}")
    log.info(f"Ping {color.l_cyan}» {color.blue}{sum(pings) / 5}ms")


async def ping_test(iterations):
    print()
    await check("https://api.minecraftservices.com/minecraft", iterations)
    # await check("https://api.mojang.com") ### Literally useless lol

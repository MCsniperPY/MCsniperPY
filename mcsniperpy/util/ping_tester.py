import asyncio
import urllib.parse
from time import perf_counter

from .logs_manager import Color as color
from .logs_manager import Logger as log


async def check(url: str):
    async def x():
        try:
            uri = urllib.parse.urlparse(url)
            reader, writer = await asyncio.open_connection(uri.hostname, 443, ssl=True)
            writer.write(f"GET {uri.path or '/'} HTTP/1.1\r\nHost:{uri.hostname}\r\n\r\n".encode())

            start = perf_counter()
            await writer.drain()

            resp = await reader.read(100)
            end = perf_counter()
            return round((end - start) * 1000)
        except Exception as e:
            log.error("Failed to connect to URL. error code: " + str(e))

    pings = []

    for _ in range(5):
        pings.append(await x())
        await asyncio.sleep(0.01)

    log.info(f"Host {color.l_cyan}» {color.blue}{urllib.parse.urlparse(url).hostname}")
    log.info(f"Ping {color.l_cyan}» {color.blue}{sum(pings) / 5}ms")


async def ping_test():
    await check("https://api.minecraftservices.com/minecraft")
    # await check("https://api.mojang.com") ### Literally useless lol

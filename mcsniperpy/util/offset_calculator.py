import asyncio
import math
import time
from statistics import mean

import aiohttp

from mcsniperpy.util import request_manager
from mcsniperpy.util import utils as util
from mcsniperpy.util.logs_manager import Color as color
from mcsniperpy.util.logs_manager import Logger as log


class OffsetCalculator:
    def __init__(self, req_count=3, accuracy=20, aim_for=.15):
        self.session = request_manager.RequestManager(
            None  # aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=300),headers={})
        )

        self.aim_for = aim_for

        self.accounts = util.parse_accs_string("email:pass")

        self.req_count = req_count

        self.log = log
        self.color = color

        self.offset = -100
        self.accuracy = accuracy

    async def run(self):

        self.session.session = aiohttp.ClientSession(headers={})

        while True:
            droptime = math.floor(time.time() + 3)
            self.accounts = util.parse_accs_string("email:pass")
            log.info(f"testing offset {self.offset} in {round(droptime - time.time())} seconds")
            res = await self.offset_test(droptime, 'test', self.offset, 3)
            if res is not True:
                self.offset += res

    async def offset_test(self, droptime, target, offset, req_count):

        pre_snipe_coroutines = [acc.snipe_connect() for _ in range(req_count) for acc in self.accounts]  # For later use

        now = time.time()
        time_until_connect = 0 if now > (droptime - 20) else (droptime - 20) - now

        self.log.debug(f'Connecting in {time_until_connect} seconds.')

        await asyncio.sleep(time_until_connect)

        await asyncio.gather(*pre_snipe_coroutines)  # Connects

        snipe_coroutines = [
            acc.snipe(acc.readers_writers[i][1], do_log=False) for i in range(self.req_count) for acc in self.accounts
        ]  # Send requests

        while time.time() < droptime - offset / 1000:
            await asyncio.sleep(0.00001)  # bad timing solution but it's fairly accurate
        # According to my tests this was .0004 seconds late while the other method (asyncio.sleep) was .004 seoncds late.

        await asyncio.gather(*snipe_coroutines)  # Sends the snipe requests
        responses = await asyncio.gather(
            *[acc.snipe_read(target, acc.readers_writers[i][0], acc.readers_writers[i][1], do_log=True  # ugly code lol
                             ) for i in range(req_count) for acc in self.accounts]
        )  # Reads the responses

        target_time = droptime + self.aim_for  # Find the actual target time

        average_time = mean([req_time for _, _, req_time in responses])  # Finds the mean request time

        diff = -(target_time - average_time) * 1000
        if self.accuracy > diff > 0:
            log.info(f"{color.white}[{color.green}success{color.white}]{color.reset} {offset} is a good offset!")
            return True
        else:
            return round(diff)

    def on_shutdown(self):
        if self.session.session is not None:
            asyncio.run(self.session.session.close())
        if self.log is not None:
            self.log.shutdown()


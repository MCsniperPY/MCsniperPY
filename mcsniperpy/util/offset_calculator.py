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
    def __init__(self, req_count=2, accuracy=20, aim_for=0.15, do_log=True):
        self.session = request_manager.RequestManager(
            None
            # aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=300),headers={})
        )

        self.aim_for = aim_for

        self.accounts = util.parse_accs_string("email:pass")

        self.req_count = req_count

        self.log = log
        self.color = color

        self.offset = -100
        self.accuracy = accuracy

        self.do_log = do_log

    async def run(self):

        self.session.session = aiohttp.ClientSession(headers={})

        while True:
            droptime = math.floor(time.time() + 3)
            self.accounts = util.parse_accs_string("email:pass")
            if self.do_log:
                log.info(
                    f"testing offset {self.offset} in "
                    f"{round(droptime - time.time())} seconds"
                )
            res = await self.offset_test(droptime, "test", self.offset)
            if res is not True:
                self.offset += res
            else:
                return self.offset

    async def offset_test(self, droptime, target, offset):

        pre_snipe_coroutines = [
            acc.snipe_connect() for _ in range(self.req_count)
            for acc in self.accounts
        ]  # For later use

        now = time.time()
        time_until_connect = 0 if now > (droptime - 20) else (droptime - 20) - now

        await asyncio.sleep(time_until_connect)

        await asyncio.gather(*pre_snipe_coroutines)  # Connects

        snipe_coroutines = [
            acc.snipe(acc.readers_writers[i][1], do_log=False)
            for i in range(self.req_count)
            for acc in self.accounts
        ]  # Send requests

        while time.time() < droptime - offset / 1000:
            await asyncio.sleep(0.00001)  # bad timing solution but
            # it's fairly accurate

        # According to my tests this was .0004 seconds late while
        # the other method (asyncio.sleep) was .004 seconds late

        start = time.perf_counter()
        await asyncio.gather(*snipe_coroutines)  # Sends the snipe requests
        end = time.perf_counter()

        responses = await asyncio.gather(
            *[
                acc.snipe_read(
                    target,
                    acc.readers_writers[i][0],
                    acc.readers_writers[i][1],
                    do_log=self.do_log,
                )
                for i in range(self.req_count)
                for acc in self.accounts
            ]
        )  # Reads the responses
        # I swear I didn't try to make it ugly

        print(self.req_count / (end - start))

        target_time = droptime + self.aim_for  # Find the actual target time

        average_time = mean(
            [req_time for _, _, req_time in responses]
        )  # Finds the mean request time

        diff = -(target_time - average_time) * 1000
        if self.accuracy > diff > 0:
            if self.do_log:
                log.info(
                    f"{color.white}[{color.green}success{color.white}] "
                    f"{color.reset}{offset} is a good offset!"
                )
            return True

        return round(diff)

    def on_shutdown(self):
        if self.session.session is not None:
            asyncio.run(self.session.session.close())
        if self.log is not None:
            self.log.shutdown()

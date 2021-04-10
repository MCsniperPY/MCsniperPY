# pylint: disable=broad-except
import random

# pylint: disable=pointless-string-statement
"""All of this file is just to change ```py
async with session.method() as r:
```

to

```py
r, text, r_json = await request_manager.method()
```"""

USER_AGENTS = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.01",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
    "54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Linux; Ubuntu 14.04) AppleWebKit/537.36 Chromium/35.0.1870.2 Safa"
    "ri/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41."
    "0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko"
    ") Chrome/42.0.2311.135 "
    "Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, "
    "like Gecko) Version/9.0.2 Safari/601.3.9",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0",
]


# https://github.com/N0taN3rd/userAgentLists/blob/9b99634d90aac404422109f80a0f273ebc1907c5/useragents.py#L28


class RequestManager:
    def __init__(self, session):
        self.session = session
        # pylint: disable=invalid-name
        self.ua = random.choice(USER_AGENTS)

    async def get(self, *args, **kwargs):
        async with self.session.get(*args, **kwargs) as response:
            try:
                json_resp = await response.json()
            except Exception:
                json_resp = None
            return response, await response.text(), json_resp

    async def post(self, *args, **kwargs):
        async with self.session.post(*args, **kwargs) as response:
            try:
                json_resp = await response.json()
            except Exception:
                json_resp = None
            return response, await response.text(), json_resp

    async def put(self, *args, **kwargs):
        async with self.session.put(*args, **kwargs) as response:
            try:
                json_resp = await response.json()
            except Exception:
                json_resp = None
            return response, await response.text(), json_resp

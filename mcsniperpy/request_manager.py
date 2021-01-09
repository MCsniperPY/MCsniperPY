"""
All of this file is just to change ```py
async with session.method() as r:
```

to

```py
r = await request_manager.method()
```

"""


class RequestManager:

    def __init__(self, session):
        self.session = session

    def get(self, *args, **kwargs):
        async with self.session.get(*args, **kwargs) as response:
            return response

    def post(self, *args, **kwargs):
        async with self.session.post(*args, **kwargs) as response:
            return response

    def put(self, *args, **kwargs):
        async with self.session.put(*args, **kwargs) as response:
            return response

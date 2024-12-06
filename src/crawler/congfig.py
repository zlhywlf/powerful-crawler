"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from crawler.clients.FakeRedisClient import FakeRedisClient

REDIS_CLS = FakeRedisClient
REDIS_ENCODING = "utf-8"
REDIS_PARAMS = {
    "socket_timeout": 30,
    "socket_connect_timeout": 30,
    "retry_on_timeout": True,
    "encoding": REDIS_ENCODING,
}

DUPEFILTER_KEY = "dupefilter:%(timestamp)s"

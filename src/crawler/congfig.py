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

DUPE_FILTER_KEY = "dupe_filter:%(timestamp)s"

SCHEDULER_QUEUE_KEY = "%(spider)s:requests"
SCHEDULER_QUEUE_CLASS = "crawler.core.queues.PriorityQueue.PriorityQueue"

SCHEDULER_DUPE_FILTER_KEY = "%(spider)s:dupe_filter"
SCHEDULER_DUPE_FILTER_CLASS = "crawler.core.RFPDupeFilter.RFPDupeFilter"

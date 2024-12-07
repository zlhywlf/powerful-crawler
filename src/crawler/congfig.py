"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

NAME = "crawler"
REDIS_CLS = "crawler.clients.FakeRedisClient.FakeRedisClient"
REDIS_ENCODING = "utf-8"
REDIS_PARAMS = {
    "socket_timeout": 30,
    "socket_connect_timeout": 30,
    "retry_on_timeout": True,
    "encoding": REDIS_ENCODING,
}

DUPE_FILTER_KEY = "dupe_filter:%(timestamp)s"

SCHEDULER_QUEUE_KEY = "%(spider)s:requests"
SCHEDULER_QUEUE_CLASS = "crawler.framework.scrapy.PriorityQueue.PriorityQueue"

SCHEDULER_DUPE_FILTER_KEY = "%(spider)s:dupe_filter"
SCHEDULER_DUPE_FILTER_CLASS = "crawler.framework.scrapy.RFPDupeFilter.RFPDupeFilter"

LOG_FORMAT = "%(asctime)s.%(msecs)03d | %(levelname)-8s | %(name)s.%(module)s:%(funcName)s:%(lineno)d - %(message)s"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

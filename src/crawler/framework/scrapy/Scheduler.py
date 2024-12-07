"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Self, override

from scrapy import Request
from scrapy.core.scheduler import BaseScheduler
from scrapy.crawler import Crawler
from scrapy.dupefilters import BaseDupeFilter
from scrapy.spiders import Spider
from scrapy.statscollectors import StatsCollector
from scrapy.utils.misc import load_object
from twisted.internet.defer import Deferred

from crawler.clients import get_redis_from_settings
from crawler.congfig import (
    SCHEDULER_DUPE_FILTER_CLASS,
    SCHEDULER_DUPE_FILTER_KEY,
    SCHEDULER_QUEUE_CLASS,
    SCHEDULER_QUEUE_KEY,
)
from crawler.core.BaseQueue import BaseQueue
from crawler.core.QueueClient import QueueClient
from crawler.framework.scrapy.RFPDupeFilter import RFPDupeFilter


class Scheduler(BaseScheduler):
    """scheduler."""

    def __init__(
        self,
        redis: QueueClient,
        idle_before_close: int = 0,
        stats: StatsCollector | None = None,
        queue_key: str = SCHEDULER_QUEUE_KEY,
        queue_cls: str = SCHEDULER_QUEUE_CLASS,
        dupe_filter: BaseDupeFilter | None = None,
        dupe_filter_key: str = SCHEDULER_DUPE_FILTER_KEY,
        dupe_filter_cls: str = SCHEDULER_DUPE_FILTER_CLASS,
        *,
        persist: bool = False,
        flush_on_start: bool = False,
    ) -> None:
        """Init."""
        self._redis = redis
        self._persist = persist
        self._flush_on_start = flush_on_start
        self._idle_before_close = idle_before_close if idle_before_close >= 0 else 0
        self._stats = stats
        self._queue_key = queue_key
        self._queue_cls = queue_cls
        self._dupe_filter = dupe_filter
        self._dupe_filter_cls = dupe_filter_cls
        self._dupe_filter_key = dupe_filter_key
        self._spider: Spider | None = None
        self._queue: BaseQueue | None = None

    @classmethod
    @override
    def from_crawler(cls, crawler: Crawler) -> Self:
        settings = crawler.settings
        kwargs = {
            "persist": settings.getbool("SCHEDULER_PERSIST"),
            "flush_on_start": settings.getbool("SCHEDULER_FLUSH_ON_START"),
            "idle_before_close": settings.getint("SCHEDULER_IDLE_BEFORE_CLOSE"),
            "stats": crawler.stats,
        }
        optional = {
            "queue_key": "SCHEDULER_QUEUE_KEY",
            "queue_cls": "SCHEDULER_QUEUE_CLASS",
            "dupe_filter_key": "SCHEDULER_DUPE_FILTER_KEY",
            "dupe_filter_cls": "DUPEFILTER_CLASS",
        }
        for name, setting_name in optional.items():
            val = settings.get(setting_name)
            if val:
                kwargs[name] = val
        dupe_filter_cls = load_object(str(kwargs["dupe_filter_cls"]))
        kwargs["dupe_filter"] = dupe_filter_cls.from_crawler(crawler)
        redis = get_redis_from_settings(settings)
        return cls(redis=redis, **kwargs)  # type: ignore [arg-type]

    @override
    def open(self, spider: Spider) -> Deferred[None] | None:
        self._spider = spider
        self._queue = load_object(self._queue_cls)(client=self._redis, spider=spider, key=self._queue_key)
        if self._flush_on_start:
            self.flush()
        if len(self.queue):
            spider.log(f"Resuming crawl ({len(self.queue)} requests scheduled)")
        return None

    def flush(self) -> None:
        """Flash."""
        if isinstance(self._dupe_filter, RFPDupeFilter):
            self._dupe_filter.clear()
        self.queue.clear()

    @override
    def close(self, reason: str) -> Deferred[None] | None:
        if not self._persist:
            self.flush()
        return None

    @override
    def enqueue_request(self, request: Request) -> bool:
        if not request.dont_filter and self._spider and self.dupe_filter.request_seen(request):
            self.dupe_filter.log(request, self._spider)
            return False
        if self._stats:
            self._stats.inc_value("scheduler/enqueued/redis", spider=self._spider)
        self.queue.push(request)
        return True

    @override
    def next_request(self) -> Request | None:
        request = self.queue.pop(self._idle_before_close)
        if request and self._stats:
            self._stats.inc_value("scheduler/dequeued/redis", spider=self._spider)
        return request

    @override
    def has_pending_requests(self) -> bool:
        return len(self.queue) > 0

    @property
    def queue(self) -> BaseQueue:
        """Queue."""
        if self._queue is None:
            msg = "The queue cannot be None"
            raise RuntimeError(msg)
        return self._queue

    @property
    def dupe_filter(self) -> BaseDupeFilter:
        """Dupe filter."""
        if self._dupe_filter is None:
            msg = "The dupe filter cannot be None"
            raise RuntimeError(msg)
        return self._dupe_filter

    @property
    def persist(self) -> bool:
        """Persist."""
        return self._persist

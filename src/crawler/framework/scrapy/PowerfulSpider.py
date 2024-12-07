"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import time
from collections.abc import Iterable
from typing import Any, Self, override

from pydantic import TypeAdapter
from scrapy import FormRequest, Request, signals
from scrapy.crawler import Crawler
from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import Spider

from crawler.clients import get_redis_from_settings
from crawler.core.QueueClient import QueueClient


class PowerfulSpider(Spider):
    """spider."""

    def __init__(self, client: QueueClient, *args: Any, **kwargs: Any) -> None:
        """Init."""
        super().__init__(*args, **kwargs)
        self._key = "powerful_spider"
        self._batch_size = 32
        self._max_idle_time = 0
        self._client = client
        self._type_adapter = TypeAdapter(dict[str, Any])
        self._idle_start_time = 0

    @override
    def start_requests(self) -> Iterable[Request]:
        found = 0
        data = self._client.pop_priority(self._key, end=self._batch_size - 1, min_=-self._batch_size, max_=-1)
        for d in data:
            param = self._type_adapter.validate_json(d)
            url = param.pop("url")
            method = str(param.pop("method")).upper()
            meta = param.pop("meta")
            reqs = FormRequest(url=url, method=method, meta=meta, formdata=param)
            if isinstance(reqs, Iterable):
                for req in reqs:
                    yield req
                    found += 1
            if reqs:
                yield reqs
                found += 1
        if found:
            self.logger.debug(f"Read {found} requests from '{self._key}'")

    @classmethod
    @override
    def from_crawler(cls, crawler: Crawler, *args: Any, **kwargs: Any) -> Self:
        settings = crawler.settings
        client = get_redis_from_settings(settings)
        spider = super().from_crawler(crawler, *args, client=client, **kwargs)
        if isinstance(spider, PowerfulSpider):
            crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        return spider

    def spider_idle(self) -> None:
        """Spider idle."""
        if self._client.zcard(self._key) > 0:
            self._idle_start_time = int(time.time())
        for req in self.start_requests():
            if self.crawler.engine:
                self.crawler.engine.crawl(req)
        idle_time = int(time.time()) - self._idle_start_time
        if self._max_idle_time != 0 and idle_time > self._max_idle_time:
            return
        raise DontCloseSpider

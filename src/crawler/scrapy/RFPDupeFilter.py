"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import hashlib
import logging
import time
from typing import Self, override

from pydantic import TypeAdapter
from scrapy import Request, Spider
from scrapy.crawler import Crawler
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.python import to_unicode
from twisted.internet.defer import Deferred
from w3lib.url import canonicalize_url

from crawler.clients import get_redis_from_settings
from crawler.congfig import DUPE_FILTER_KEY
from crawler.core.QueueClient import QueueClient


class RFPDupeFilter(BaseDupeFilter):
    """Request fingerprint dupe filter."""

    logger = logging.getLogger(__name__)

    def __init__(self, *, redis: QueueClient, key: str, debug: bool = False) -> None:
        """Init."""
        self._redis = redis
        self._debug = debug
        self._key = key
        self._type_adapter = TypeAdapter(dict[str, str])

    @classmethod
    @override
    def from_crawler(cls, crawler: Crawler) -> Self:
        debug = crawler.settings.getbool("DUPEFILTER_DEBUG")
        redis = get_redis_from_settings(crawler.settings)
        key = DUPE_FILTER_KEY % {"timestamp": int(time.time())}
        cls.logger.info(f"dupe filter key: {key}")
        return cls(redis=redis, key=key, debug=debug)

    @override
    def request_seen(self, request: Request) -> bool:
        fp = self.request_fingerprint(request)
        added = self._redis.sadd(self._key, fp)
        return added == 0

    def request_fingerprint(self, request: Request) -> str:
        """Request fingerprint."""
        fingerprint_data = {
            "method": to_unicode(request.method),
            "url": canonicalize_url(request.url),
            "body": (request.body or b"").hex(),
        }
        fingerprint_json = self._type_adapter.dump_json(fingerprint_data)
        return hashlib.sha1(fingerprint_json).hexdigest()  # noqa: S324

    @override
    def close(self, reason: str) -> Deferred[None] | None:
        self.clear()
        return None

    def clear(self) -> None:
        """Clear fingerprint data."""
        self._redis.delete(self._key)

    @override
    def log(self, request: Request, spider: Spider) -> None:
        if self._debug:
            self.logger.debug(f"Filtered duplicate request: {request}", extra={"spider": spider})

    @property
    def redis(self) -> QueueClient:
        """Redis."""
        return self._redis

    @property
    def debug(self) -> bool:
        """Debug."""
        return self._debug

    @property
    def key(self) -> str:
        """Key."""
        return self._key

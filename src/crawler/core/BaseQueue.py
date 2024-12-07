"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import TypeAdapter
from scrapy import Request, Spider
from scrapy.utils.request import request_from_dict

from crawler.core.QueueClient import QueueClient


class BaseQueue(ABC):
    """base queue."""

    def __init__(self, redis: QueueClient, spider: Spider, key: str) -> None:
        """Init."""
        self._type_adapter = TypeAdapter(dict[str, Any])
        self._redis = redis
        self._spider = spider
        self._key = key % {"spider": spider.name}

    def encode_request(self, request: Request) -> bytes:
        """Encode a request object."""
        obj = request.to_dict(spider=self._spider)
        return self._type_adapter.dump_json(obj)

    def decode_request(self, encoded_request: bytes) -> Request:
        """Decode an request previously encoded."""
        obj = self._type_adapter.validate_json(encoded_request)
        return request_from_dict(obj, spider=self._spider)

    @abstractmethod
    def __len__(self) -> int:
        """Len."""

    @abstractmethod
    def push(self, request: Request) -> None:
        """Push."""

    @abstractmethod
    def pop(self, timeout: int = 0) -> Request | None:
        """Pop."""

    def clear(self) -> None:
        """Clear."""
        self._redis.delete(self._key)

    @property
    def redis(self) -> QueueClient:
        """Redis."""
        return self._redis

    @property
    def key(self) -> str:
        """Key."""
        return self._key

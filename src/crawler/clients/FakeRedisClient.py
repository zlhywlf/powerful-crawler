"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any, override

from fakeredis import FakeAsyncRedis

from crawler.core.RedisClient import RedisClient


class FakeRedisClient(RedisClient):
    """fake redis client."""

    def __init__(self, redis: FakeAsyncRedis) -> None:
        """Init."""
        self._redis = redis

    @classmethod
    @override
    def from_url(cls, url: str, **kwargs: Any) -> RedisClient:
        """Create client."""
        return cls(FakeAsyncRedis())

    @override
    async def set(self, name: str, value: str | float) -> None:
        await self._redis.set(name, value)

    @override
    async def get(self, name: str) -> Any:
        return await self._redis.get(name)

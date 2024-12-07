"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any, Self, override

from fakeredis import FakeStrictRedis

from crawler.core.QueueClient import QueueClient


class FakeRedisClient(QueueClient):
    """fake redis client."""

    def __init__(self, redis: FakeStrictRedis) -> None:
        """Init."""
        self._redis = redis

    @classmethod
    @override
    def from_url(cls, url: str, **kwargs: Any) -> Self:
        """Create client."""
        return cls(FakeStrictRedis())

    @override
    def set(self, name: str, value: str | float) -> None:
        self._redis.set(name, value)

    @override
    def get(self, name: str) -> Any:
        return self._redis.get(name)

    @override
    def sadd(self, name: str, value: str | float) -> int:
        res = self._redis.sadd(name, value)
        return res if isinstance(res, int) else -1

    @override
    def delete(self, name: str) -> None:
        self._redis.delete(name)

    @override
    def zcard(self, name: str) -> int:
        res = self._redis.zcard(name)
        return res if isinstance(res, int) else -1

    @override
    def execute_command(self, *args: Any, **options: Any) -> None:
        self._redis.execute_command(*args, **options)  # type:ignore [no-untyped-call]

    @override
    def pop_priority(self, key: str, start: int = 0, end: int = 0, min_: int = 0, max_: int = 0) -> list[Any]:
        with self._redis.pipeline() as pip:
            pip.multi()
            pip.zrevrange(key, start, end)
            pip.zremrangebyrank(key, min_, max_)
            results: list[Any] = pip.execute()[0]  # type:ignore  [no-untyped-call]
        return results

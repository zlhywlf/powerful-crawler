"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from faker import Faker

from crawler.clients import get_redis
from crawler.congfig import REDIS_CLS


async def test_default_instance(faker: Faker) -> None:
    """Test default instance."""
    redis = get_redis()
    k = faker.name()
    v = faker.name()
    await redis.set(k, v)
    assert isinstance(redis, REDIS_CLS)
    assert await redis.get(k) == v.encode()

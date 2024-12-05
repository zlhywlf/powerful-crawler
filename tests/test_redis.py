"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from faker import Faker
from pytest_mock import MockerFixture

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


async def test_custom_class(faker: Faker, mocker: MockerFixture) -> None:
    """Test custom class."""
    redis_cls = mocker.Mock()
    url = faker.url()
    other = faker.name()
    redis = get_redis(redis_cls=redis_cls, url=url, other=other)
    assert redis is redis_cls.from_url.return_value
    redis_cls.from_url.assert_called_with(url, other=other)

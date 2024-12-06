"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from faker import Faker
from pytest_mock import MockerFixture
from scrapy.settings import Settings

from crawler.clients import get_redis, get_redis_from_settings
from crawler.congfig import REDIS_CLS, REDIS_PARAMS


def test_default_instance(faker: Faker) -> None:
    """Test default instance."""
    redis = get_redis()
    k = faker.name()
    v = faker.name()
    redis.set(k, v)
    assert isinstance(redis, REDIS_CLS)
    assert redis.get(k) == v.encode()


def test_custom_class(faker: Faker, mocker: MockerFixture) -> None:
    """Test custom class."""
    redis_cls = mocker.Mock()
    url = faker.url()
    other = faker.name()
    redis = get_redis(redis_cls=redis_cls, url=url, other=other)
    assert redis is redis_cls.from_url.return_value
    redis_cls.from_url.assert_called_with(url=url, other=other)


def test_default_instance_from_settings() -> None:
    """Test default instance from settings."""
    redis = get_redis_from_settings(Settings())
    assert isinstance(redis, REDIS_CLS)


def test_custom_class_from_settings() -> None:
    """Test custom class from settings."""
    settings = Settings({
        "REDIS_CLS": f"{REDIS_CLS.__module__}.{REDIS_CLS.__name__}",
    })
    redis = get_redis_from_settings(settings)
    assert isinstance(redis, REDIS_CLS)


def test_params_from_settings(faker: Faker, mocker: MockerFixture) -> None:
    """Test default params from settings."""
    expected_params = {"timeout": faker.random_digit(), "flag": faker.boolean(), "url": faker.url()}
    redis_cls = mocker.Mock()
    settings = Settings({"REDIS_CLS": redis_cls, "REDIS_PARAMS": expected_params})
    redis = get_redis_from_settings(settings)
    assert redis is redis_cls.from_url.return_value
    expected_params = expected_params | REDIS_PARAMS
    redis_cls.from_url.assert_called_with(**expected_params)

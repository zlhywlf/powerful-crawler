"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import pytest
from faker import Faker
from pytest_mock import MockerFixture, MockType
from scrapy import Request
from scrapy.settings import Settings

from crawler.framework.scrapy.RFPDupeFilter import DUPE_FILTER_KEY, RFPDupeFilter  # type:ignore [attr-defined]


@pytest.fixture
def db() -> dict[str, set[str]]:
    """Redis db."""
    return {}


@pytest.fixture
def key(faker: Faker) -> str:
    """Key."""
    return faker.name()


@pytest.fixture
def redis(mocker: MockerFixture, db: dict[str, set[str]]) -> MockType:
    """Redis client."""
    redis: MockType = mocker.Mock()

    def sadd(key: str, fp: str, added: int = 0) -> int:
        fingerprints = db.setdefault(key, set())
        if fp not in fingerprints:
            fingerprints.add(fp)
            added += 1
        return added

    redis.sadd = sadd
    return redis


@pytest.fixture
def dupe_filter(redis: MockType, key: str) -> RFPDupeFilter:
    """Dupe filter."""
    return RFPDupeFilter(redis=redis, key=key)


def test_request_seen(faker: Faker, dupe_filter: RFPDupeFilter) -> None:
    """Test request seen."""
    url = faker.unique.url()
    req01 = Request(url, method=faker.unique.http_method())
    req02 = Request(url, method=faker.unique.http_method())
    req03 = Request(faker.unique.url())
    assert not dupe_filter.request_seen(req01)
    assert dupe_filter.request_seen(req01)
    assert not dupe_filter.request_seen(req02)
    assert not dupe_filter.request_seen(req03)


def test_overridable_request_fingerprint(faker: Faker, dupe_filter: RFPDupeFilter, mocker: MockerFixture) -> None:
    """Test overridable request fingerprint."""
    req = Request(faker.url())
    dupe_filter.request_fingerprint = mocker.Mock(wraps=dupe_filter.request_fingerprint)  # type:ignore [method-assign]
    assert not dupe_filter.request_seen(req)
    dupe_filter.request_fingerprint.assert_called_with(req)  # type:ignore  [attr-defined]


def test_clear_delete(dupe_filter: RFPDupeFilter, redis: MockType, key: str) -> None:
    """Test clear delete."""
    dupe_filter.clear()
    redis.delete.assert_called_with(key)


def test_close_calls_clear(faker: Faker, dupe_filter: RFPDupeFilter, mocker: MockerFixture) -> None:
    """Test close calls clear."""
    dupe_filter.clear = mocker.Mock(wraps=dupe_filter.clear)  # type:ignore [method-assign]
    dupe_filter.close(faker.name())
    dupe_filter.close(faker.name())
    assert dupe_filter.clear.call_count == 2  # type:ignore  [attr-defined]


def test_log(faker: Faker, redis: MockType, mocker: MockerFixture) -> None:
    """Test log."""
    dupes = faker.random_int(1, 10)

    def _test(df: RFPDupeFilter, log_count: int) -> None:
        df.logger.debug = mocker.Mock(wraps=df.logger.debug)  # type:ignore [method-assign]
        url = faker.url()
        for _ in range(dupes):
            req = Request(url)
            df.log(req, spider=mocker.Mock())
        assert df.logger.debug.call_count == log_count  # type:ignore  [attr-defined]

    df01 = RFPDupeFilter(redis=redis, key=faker.name())
    _test(df01, 0)
    df02 = RFPDupeFilter(redis=redis, key=faker.name(), debug=True)
    _test(df02, dupes)


def test_from_crawler(mocker: MockerFixture) -> None:
    """Test from crawler."""
    get_redis_from_settings = mocker.patch(f"{RFPDupeFilter.__module__}.get_redis_from_settings")
    settings = Settings({
        "DUPEFILTER_DEBUG": True,
    })
    crawler = mocker.Mock(settings=settings)
    df: RFPDupeFilter = RFPDupeFilter.from_crawler(crawler)
    assert df.redis is get_redis_from_settings.return_value
    assert df.debug
    assert df.key.startswith(DUPE_FILTER_KEY.split(":")[0])

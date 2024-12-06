"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import pytest
from faker import Faker
from pytest_mock import MockerFixture
from scrapy import Request
from scrapy.crawler import Crawler
from scrapy.utils.test import get_crawler

from crawler.core.Scheduler import Scheduler


@pytest.fixture
def crawler(faker: Faker) -> Crawler:
    """Crawler."""
    return get_crawler(
        settings_dict={
            "REDIS_HOST": faker.hostname(),
            "REDIS_PORT": faker.port_number(),
            "SCHEDULER_QUEUE_KEY": faker.name(),
            "SCHEDULER_DUPE_FILTER_KEY": faker.user_name(),
            "SCHEDULER_FLUSH_ON_START": False,
            "SCHEDULER_PERSIST": False,
            "DUPEFILTER_CLASS": "crawler.core.RFPDupeFilter.RFPDupeFilter",
        }
    )


@pytest.fixture
def scheduler(crawler: Crawler) -> Scheduler:
    """Scheduler."""
    return Scheduler.from_crawler(crawler)


def test_scheduler(crawler: Crawler, scheduler: Scheduler, faker: Faker) -> None:
    """Test scheduler."""
    assert not scheduler.persist
    scheduler.open(crawler.spidercls())
    assert len(scheduler.queue) == 0
    req = Request(faker.url())
    scheduler.enqueue_request(req)
    assert scheduler.has_pending_requests()
    assert len(scheduler.queue) == 1
    scheduler.enqueue_request(req)
    assert len(scheduler.queue) == 1
    out = scheduler.next_request()
    assert out
    assert out.url == req.url
    assert not scheduler.has_pending_requests()
    assert len(scheduler.queue) == 0
    scheduler.close(faker.name())


def test_scheduler_persistent(crawler: Crawler, scheduler: Scheduler, faker: Faker, mocker: MockerFixture) -> None:
    """Test scheduler persistent."""
    spider = crawler.spidercls()
    spider.log = mocker.Mock(spec=spider.log)  # type: ignore  [method-assign]
    scheduler._persist = True
    scheduler.open(spider)
    assert spider.log.call_count == 0  # type: ignore   [attr-defined]
    scheduler.enqueue_request(Request(faker.unique.url()))
    scheduler.enqueue_request(Request(faker.unique.url()))
    assert scheduler.has_pending_requests()
    scheduler.close(faker.name())
    scheduler.open(spider)
    spider.log.assert_has_calls([mocker.call("Resuming crawl (2 requests scheduled)")])  # type: ignore   [attr-defined]
    assert len(scheduler.queue) == 2
    scheduler._persist = False
    scheduler.close(faker.name())
    assert len(scheduler.queue) == 0

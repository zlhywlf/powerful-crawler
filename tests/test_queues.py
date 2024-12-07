"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import pytest
from faker import Faker
from scrapy import Request, Spider

from crawler.clients.FakeRedisClient import FakeRedisClient
from crawler.core.BaseQueue import BaseQueue
from crawler.core.QueueClient import QueueClient
from crawler.framework.scrapy.PriorityQueue import PriorityQueue


@pytest.fixture
def redis(faker: Faker) -> QueueClient:
    """Redis client."""
    return FakeRedisClient.from_url(faker.url())


@pytest.mark.parametrize("q_cls", [PriorityQueue])
def test_clear(redis: QueueClient, faker: Faker, q_cls: type[BaseQueue]) -> None:
    """Test clear."""
    q = q_cls(redis, Spider(faker.name()), faker.name())
    assert len(q) == 0
    num = faker.random_int(1, 10)
    for i in range(num):
        req = Request(f"{faker.url()}/{i}")
        q.push(req)
    assert len(q) == num
    q.clear()
    assert len(q) == 0


def test_priority_queue(redis: QueueClient, faker: Faker) -> None:
    """Test priority queue."""
    q = PriorityQueue(redis, Spider(faker.name()), faker.name())
    req01 = Request(faker.unique.url(), priority=100)
    req02 = Request(faker.unique.url(), priority=50)
    req03 = Request(faker.unique.url(), priority=200)
    q.push(req01)
    q.push(req02)
    q.push(req03)
    out01 = q.pop()
    out02 = q.pop()
    out03 = q.pop()
    assert out01
    assert out01.url == req03.url
    assert out02
    assert out02.url == req01.url
    assert out03
    assert out03.url == req02.url


@pytest.mark.parametrize("q_cls", [PriorityQueue])
def test_encode_decode_requests(redis: QueueClient, faker: Faker, q_cls: type[BaseQueue]) -> None:
    """Test encode decode requests."""
    spider = Spider(faker.name())
    q = q_cls(redis, spider, faker.name())
    req = Request(faker.url(), callback=spider.parse, meta={faker.name(): faker.name()})
    out = q.decode_request(q.encode_request(req))
    assert out.url == req.url
    assert out.meta == req.meta
    assert out.callback == req.callback

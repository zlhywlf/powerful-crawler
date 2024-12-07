"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import json
import threading
from collections.abc import AsyncGenerator, Callable
from typing import Any

import scrapy
from scrapy.http.response import Response
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import INTEGER, VARCHAR
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import Column, Field, SQLModel

from crawler.framework.scrapy.PowerfulSpider import PowerfulSpider


class Url(SQLModel, table=True):
    """url."""

    id: int = Field(None, sa_column=Column(INTEGER(), primary_key=True))
    url: str = Field(None, sa_column=Column(VARCHAR()))


class SpiderItem(scrapy.Item):
    """model."""

    author = scrapy.Field()
    text = scrapy.Field()


async def parse(obj: scrapy.Spider, response: Response) -> AsyncGenerator[Any, None]:
    """Parse."""
    for quote in response.css("div.quote"):
        yield SpiderItem(
            author=quote.xpath("span/small/text()").get(),
            text=quote.css("span.text::text").get(),
        )

    next_page = response.css('li.next a::attr("href")').get()
    if next_page is not None:
        yield response.follow(next_page, obj.parse)


async def process_item(obj: object, item: SpiderItem, spider: scrapy.Spider) -> SpiderItem:  # noqa: ARG001
    """Process item."""
    spider.log(item)
    return item


async def init() -> None:
    """Init."""
    configs: list[Url] = []
    g = globals()
    engine = create_async_engine("sqlite+aiosqlite://", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin():
            session.add_all([Url(url="https://quotes.toscrape.com/tag/humor/")])
        stmt = select(Url)
        result = await session.execute(stmt)
        configs = list(result.scalars())
    await engine.dispose()
    name = "Quotes"
    spider_name = f"{name}Spider"
    pipeliner_name = f"{name}Pipeline"
    g.setdefault(
        spider_name,
        type(
            spider_name,
            (PowerfulSpider,),
            {
                "name": name,
                "custom_settings": {
                    "LOG_FORMAT": "%(asctime)s.%(msecs)03d | %(levelname)-8s | "
                    "%(name)s.%(module)s:%(funcName)s:%(lineno)d - %(message)s",
                    "ITEM_PIPELINES": {f"crawler.spiders.{pipeliner_name}": 1},
                    "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
                },
                "parse": parse,
            },
        ),
    )
    g.setdefault(pipeliner_name, type(pipeliner_name, (), {"process_item": process_item}))

    def wrapper(func: type) -> Callable[[Any], None]:
        def w(s: PowerfulSpider, *args: Any, **kwargs: Any) -> None:
            func(s, *args, **kwargs)
            threading.Timer(
                2,
                lambda: [
                    s._client.execute_command(
                        "ZADD",
                        "powerful_spider",
                        1,
                        json.dumps({
                            "url": _.url,
                            "method": "GET",
                            "meta": {"a": 1},
                        }),
                    )
                    for _ in configs
                ],
            ).start()
            threading.Timer(
                2,
                lambda: setattr(s, "_max_idle_time", 1),
            ).start()

        return w

    cls = g.get(spider_name)
    cls.__init__ = wrapper(cls.__init__)  # type:ignore  [misc]

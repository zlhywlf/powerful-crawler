"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import json
import threading
from collections.abc import Callable, Generator
from typing import Any

import scrapy
from scrapy.http.response import Response
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import INTEGER, VARCHAR
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload
from sqlmodel import Column, Field, ForeignKey, Relationship, SQLModel

from crawler.framework.scrapy.PowerfulSpider import PowerfulSpider


class Spider(SQLModel, table=True):
    """Spider."""

    id: int = Field(None, sa_column=Column(INTEGER(), primary_key=True))
    name: str = Field(None, sa_column=Column(VARCHAR()))
    parse: str = Field(None, sa_column=Column(VARCHAR()))
    process_item: str = Field(None, sa_column=Column(VARCHAR()))
    start_urls: list["Url"] = Relationship()


class Url(SQLModel, table=True):
    """url."""

    id: int = Field(None, sa_column=Column(INTEGER(), primary_key=True))
    spider_id: int = Field(None, sa_column=Column(INTEGER(), ForeignKey("spider.id")))
    url: str = Field(None, sa_column=Column(VARCHAR()))


class SpiderItem(scrapy.Item):
    """model."""

    author = scrapy.Field()
    text = scrapy.Field()


def parse(obj: scrapy.Spider, response: Response) -> Generator[Any, Any, None]:
    """Parse."""
    for quote in response.css("div.quote"):
        yield SpiderItem(
            author=quote.xpath("span/small/text()").get(),
            text=quote.css("span.text::text").get(),
        )

    next_page = response.css('li.next a::attr("href")').get()
    if next_page is not None:
        yield response.follow(next_page, obj.parse)


def process_item(obj: object, item: SpiderItem, spider: scrapy.Spider) -> SpiderItem:  # noqa: ARG001
    """Process item."""
    spider.log(item)
    return item


async def init() -> None:
    """Init."""
    configs: list[Spider] = []
    g = globals()
    engine = create_async_engine("sqlite+aiosqlite://", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin():
            session.add_all([
                Spider(
                    name="Quotes",
                    parse="parse",
                    process_item="process_item",
                    start_urls=[Url(spider_id=1, url="https://quotes.toscrape.com/tag/humor/")],
                )
            ])
        stmt = select(Spider).options(selectinload(Spider.start_urls))  # type:ignore  [arg-type]
        result = await session.execute(stmt)
        configs = list(result.scalars())
    await engine.dispose()
    for config in configs:
        name = config.name
        spider_name = f"{name}Spider"
        pipeliner_name = f"{name}Pipeline"
        parse_func = g[config.parse]
        process_item_func = g[config.process_item]
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
                    "start_urls": [_.url for _ in config.start_urls],
                    "parse": parse_func,
                },
            ),
        )
        g.setdefault(pipeliner_name, type(pipeliner_name, (), {"process_item": process_item_func}))

        def wrapper(func: type) -> Callable[[Any], None]:
            def w(s: PowerfulSpider, *args: Any, **kwargs: Any) -> None:
                func(s, *args, **kwargs)
                threading.Timer(
                    2,
                    lambda: s._client.execute_command(
                        "ZADD",
                        "powerful_spider",
                        1,
                        json.dumps({
                            "url": "https://quotes.toscrape.com/tag/humor/",
                            "method": "GET",
                            "meta": {"a": 1},
                        }),
                    ),
                ).start()
                threading.Timer(
                    2,
                    lambda: setattr(s, "_max_idle_time", 1),
                ).start()

            return w

        cls = g.get(spider_name)
        cls.__init__ = wrapper(cls.__init__)  # type:ignore  [misc]

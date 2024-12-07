"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import asyncio
import json
import threading
from collections.abc import AsyncGenerator, Callable
from typing import Any

import scrapy
from scrapy.http.response import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from crawler.congfig import LOG_FORMAT, NAME, REDIS_CLS, TWISTED_REACTOR
from crawler.framework.scrapy.PowerfulSpider import PowerfulSpider
from crawler.models.Result import Result
from crawler.models.Target import Target


async def parse(obj: scrapy.Spider, response: Response) -> AsyncGenerator[Any, None]:
    """Parse."""
    for quote in response.css("div.quote"):
        yield Result(
            author=quote.xpath("span/small/text()").get(),
            text=quote.css("span.text::text").get(),
        )

    next_page = response.css('li.next a::attr("href")').get()
    if next_page is not None:
        yield response.follow(next_page, obj.parse)


async def process_item(obj: object, item: Result, spider: scrapy.Spider) -> Result:  # noqa: ARG001
    """Process item."""
    spider.log(item)
    return item


g = globals()
spider_name = f"{NAME}Spider"
pipeliner_name = f"{NAME}Pipeline"
g.setdefault(
    spider_name,
    type(
        spider_name,
        (PowerfulSpider,),
        {
            "name": NAME,
            "custom_settings": {
                "LOG_FORMAT": LOG_FORMAT,
                "ITEM_PIPELINES": {f"crawler.spiders.{pipeliner_name}": 1},
                "TWISTED_REACTOR": TWISTED_REACTOR,
                "REDIS_CLS": REDIS_CLS,
            },
            "parse": parse,
        },
    ),
)
g.setdefault(pipeliner_name, type(pipeliner_name, (), {"process_item": process_item}))


async def init() -> None:
    """Init."""
    targets: list[Target] = []
    engine = create_async_engine("sqlite+aiosqlite://", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin():
            session.add_all([Target(url="https://quotes.toscrape.com/tag/humor/")])
        stmt = select(Target)
        result = await session.execute(stmt)
        targets = list(result.scalars())
    await engine.dispose()

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
                    for _ in targets
                ],
            ).start()
            threading.Timer(
                2,
                lambda: setattr(s, "_max_idle_time", 1),
            ).start()

        return w

    cls = g.get(spider_name)
    cls.__init__ = wrapper(cls.__init__)  # type:ignore  [misc]


asyncio.run(init())

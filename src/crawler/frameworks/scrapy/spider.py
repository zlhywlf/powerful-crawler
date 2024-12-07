"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import asyncio
import json
import threading
from collections.abc import Callable
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from crawler.congfig import LOG_FORMAT, NAME, REDIS_CLS
from crawler.frameworks.scrapy.PowerfulSpider import PowerfulSpider
from crawler.models.Target import Target
from crawler.pasers.MasterPaser import MasterPaser
from crawler.processors.MasterProcessor import MasterProcessor

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
                "ITEM_PIPELINES": {f"crawler.frameworks.scrapy.spider.{pipeliner_name}": 1},
                "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
                "REDIS_CLS": REDIS_CLS,
            },
            "parse": MasterPaser(),
        },
    ),
)
g.setdefault(pipeliner_name, type(pipeliner_name, (), {"process_item": MasterProcessor()}))


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
            session.add_all([Target(url="https://quotes.toscrape.com/tag/humor/", method="get")])
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
                            "method": _.method,
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

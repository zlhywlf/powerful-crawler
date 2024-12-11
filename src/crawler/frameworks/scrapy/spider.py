"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import asyncio
import threading
from collections.abc import Callable
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from crawler.congfig import LOG_FORMAT, NAME, REDIS_CLS
from crawler.decisions.pasers.nodes.ListPageDecisionNode import ListPageDecisionNode
from crawler.decisions.pasers.nodes.NextPageDecisionNode import NextPageDecisionNode
from crawler.decisions.pasers.nodes.PagingDecisionNode import PagingDecisionNode
from crawler.frameworks.scrapy.PowerfulSpider import PowerfulSpider
from crawler.frameworks.scrapy.ScrapyPaser import ScrapyPaser
from crawler.frameworks.scrapy.ScrapyProcessor import ScrapyProcessor
from crawler.models.po.Base import Base
from crawler.models.po.MetaInfo import MetaInfo
from crawler.models.po.TaskInfo import TaskInfo

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
            "parse": ScrapyPaser(),
        },
    ),
)
g.setdefault(pipeliner_name, type(pipeliner_name, (), {"process_item": ScrapyProcessor()}))


async def init(index: int) -> None:
    """Init."""
    engine = create_async_engine("sqlite+aiosqlite://", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin():
            session.add_all([
                TaskInfo(
                    url="https://quotes.toscrape.com/tag/humor/",
                    method="get",
                    meta=MetaInfo(
                        name="quotes",
                        meta=[
                            MetaInfo(
                                name="NextPageDecisionNode",
                                meta=[
                                    MetaInfo(
                                        name="SavePageDecisionNode",
                                        type=1,
                                    )
                                ],
                                config=NextPageDecisionNode.Config(
                                    needed=True, next_path='li.next a::attr("href")', type="css"
                                ).model_dump_json(),
                            ),
                            MetaInfo(
                                name="SavePageDecisionNode",
                                type=1,
                            ),
                        ],
                    ),
                ),
                TaskInfo(
                    url="https://www.hbggzypm.cn//jynoticeController/tojynoticelist",
                    method="get",
                    meta=MetaInfo(
                        name="湖北省公共资源产权交易网-paging",
                        meta=[
                            MetaInfo(
                                name="PagingDecisionNode",
                                meta=[
                                    MetaInfo(
                                        name="湖北省公共资源产权交易网-list",
                                        meta=[
                                            MetaInfo(
                                                name="ListPageDecisionNode",
                                                meta=[
                                                    MetaInfo(
                                                        name="湖北省公共资源产权交易网-detail",
                                                        meta=[
                                                            MetaInfo(
                                                                name="SavePageDecisionNode",
                                                            )
                                                        ],
                                                    )
                                                ],
                                                config=ListPageDecisionNode.Config(
                                                    paths="//tr//a[@title]/@href",
                                                    names="//tr//a/@title",
                                                ).model_dump_json(),
                                            )
                                        ],
                                    )
                                ],
                                config=PagingDecisionNode.Config(
                                    limit=r"var\s+limitcount\s*=\s*(\d+)",
                                    count=r'count\s*:\s*["\']?(\d+)["\']?,',
                                    url=r'url\s*:\s*[\'"]([^\'"]+)[\'"]',
                                ).model_dump_json(),
                            )
                        ],
                    ),
                ),
            ])
        stmt = select(TaskInfo).where(TaskInfo.id == index)
        result = (await session.execute(stmt)).scalar()
        if not result:
            raise RuntimeError
        task = TaskInfo.load_task(result)
    await engine.dispose()

    def wrapper(func: type) -> Callable[[Any], None]:
        def w(s: PowerfulSpider, *args: Any, **kwargs: Any) -> None:
            func(s, *args, **kwargs)
            threading.Timer(
                2,
                lambda: s._client.execute_command(
                    "ZADD",
                    "powerful_spider",
                    1,
                    task.model_dump_json(),
                ),
            ).start()
            threading.Timer(
                2,
                lambda: setattr(s, "_max_idle_time", 1),
            ).start()

        return w

    cls = g.get(spider_name)
    cls.__init__ = wrapper(cls.__init__)  # type:ignore  [misc]


asyncio.run(init(1))

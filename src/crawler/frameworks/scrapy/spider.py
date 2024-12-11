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
from crawler.frameworks.scrapy.PowerfulSpider import PowerfulSpider
from crawler.frameworks.scrapy.ScrapyPaser import ScrapyPaser
from crawler.frameworks.scrapy.ScrapyProcessor import ScrapyProcessor
from crawler.models.po.Base import Base
from crawler.models.po.MetaConfig import MetaConfig
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
                        type=0,
                        meta=[
                            MetaInfo(
                                name="NextPageDecisionNode",
                                type=0,
                                meta=[
                                    MetaInfo(
                                        name="SavePageDecisionNode",
                                        type=1,
                                        meta=[],
                                        config=[],
                                    )
                                ],
                                config=[
                                    MetaConfig(name="needed", value="True", type="bool"),
                                    MetaConfig(name="next_path", value='li.next a::attr("href")', type="str"),
                                    MetaConfig(name="type", value="css", type="str"),
                                ],
                            ),
                            MetaInfo(
                                name="SavePageDecisionNode",
                                type=1,
                                meta=[],
                                config=[],
                            ),
                        ],
                        config=[],
                    ),
                ),
                TaskInfo(
                    url="https://www.hbggzypm.cn//jynoticeController/tojynoticelist",
                    method="get",
                    meta=MetaInfo(
                        name="湖北省公共资源产权交易网-paging",
                        type=0,
                        meta=[
                            MetaInfo(
                                name="PagingDecisionNode",
                                type=0,
                                meta=[
                                    MetaInfo(
                                        name="湖北省公共资源产权交易网-list",
                                        type=0,
                                        meta=[
                                            MetaInfo(
                                                name="ListPageDecisionNode",
                                                type=0,
                                                meta=[
                                                    MetaInfo(
                                                        name="湖北省公共资源产权交易网-detail",
                                                        type=0,
                                                        meta=[
                                                            MetaInfo(
                                                                name="SavePageDecisionNode",
                                                                type=0,
                                                                meta=[],
                                                                config=[],
                                                            )
                                                        ],
                                                        config=[],
                                                    )
                                                ],
                                                config=[
                                                    MetaConfig(name="paths", value="//tr//a[@title]/@href", type="str"),
                                                    MetaConfig(name="names", value="//tr//a/@title", type="str"),
                                                ],
                                            )
                                        ],
                                        config=[],
                                    )
                                ],
                                config=[
                                    MetaConfig(name="needed", value="False", type="bool"),
                                    MetaConfig(name="limit", value=r"var\s+limitcount\s*=\s*(\d+)", type="str"),
                                    MetaConfig(name="count", value=r'count\s*:\s*["\']?(\d+)["\']?,', type="str"),
                                    MetaConfig(name="url", value=r'url\s*:\s*[\'"]([^\'"]+)[\'"]', type="str"),
                                ],
                            )
                        ],
                        config=[],
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

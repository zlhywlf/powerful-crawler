"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import asyncio
import os
from collections.abc import Generator
from pathlib import Path
from typing import Any

import scrapy
from scrapy.http.response import Response
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import INTEGER, VARCHAR
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload
from sqlmodel import Column, Field, ForeignKey, Relationship, SQLModel

db = Path(os.environ["USERPROFILE"]) / "Projects" / "public" / "laboratory" / "identifier.sqlite"
_configs: list["Spider"] = []
g = globals()


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


async def main() -> None:
    """Main."""
    global _configs
    engine = create_async_engine(f"sqlite+aiosqlite:///{db}", echo=True)
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
        _configs = list(result.scalars())
    await engine.dispose()


asyncio.run(main())


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


for config in _configs:
    name = config.name
    spider_name = f"{name}Spider"
    pipeliner_name = f"{name}Pipeline"
    parse_func = g[config.parse]
    process_item_func = g[config.process_item]
    g.setdefault(
        spider_name,
        type(
            spider_name,
            (scrapy.Spider,),
            {
                "name": name,
                "custom_settings": {
                    "LOG_FORMAT": "%(asctime)s.%(msecs)03d | %(levelname)-8s | "
                    "%(name)s.%(module)s:%(funcName)s:%(lineno)d - %(message)s",
                    "ITEM_PIPELINES": {f"crawler.spiders.{pipeliner_name}": 1},
                },
                "start_urls": [_.url for _ in config.start_urls],
                "parse": parse_func,
            },
        ),
    )
    g.setdefault(pipeliner_name, type(pipeliner_name, (), {"process_item": process_item_func}))

"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import asyncio

import scrapy

from crawler.models.Result import Result


class MasterProcessor:
    """master processor."""

    async def __call__(self, item: Result, spider: scrapy.Spider) -> Result:
        """Do."""
        spider.log(f"{item.id},{item.type},{len(item.content)}")
        loop = asyncio.get_event_loop()
        with open(f"{item.id}_{len(item.content)}.{'html' if 'html' in item.type else 'unknown'}", "wb") as f:  # noqa: ASYNC230 PTH123
            await loop.run_in_executor(None, f.write, item.content)
        return item

"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import scrapy

from crawler.models.Result import Result


class MasterProcessor:
    """master processor."""

    async def __call__(self, item: Result, spider: scrapy.Spider) -> Result:
        """Do."""
        spider.log(f"{item.id},{item.type},{len(item.content)}")
        return item

"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import AsyncGenerator
from typing import Any

from scrapy.http.response import Response

from crawler.models.Context import Context
from crawler.models.Meta import Meta
from crawler.pasers.NextPageDecisionNode import NextPageDecisionNode
from crawler.pasers.ParserDecisionEngine import ParserDecisionEngine


class MasterPaser:
    """master paser."""

    async def __call__(self, response: Response) -> AsyncGenerator[Any, None]:
        """Parse."""
        engine = ParserDecisionEngine(
            Meta(name="NextPageDecisionNode", type=-1), {"NextPageDecisionNode": NextPageDecisionNode()}
        )
        results = await engine.process(Context(url=response.url, meta=response.meta))
        for result in results:
            yield result

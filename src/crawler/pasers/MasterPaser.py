"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import AsyncGenerator
from typing import Any

from scrapy.http.response import Response

from crawler.models.Context import Context
from crawler.models.Meta import Meta
from crawler.pasers.ListPageDecisionNode import ListPageDecisionNode
from crawler.pasers.NextPageDecisionNode import NextPageDecisionNode
from crawler.pasers.PagingDecisionNode import PagingDecisionNode
from crawler.pasers.ParserDecisionEngine import ParserDecisionEngine
from crawler.pasers.SavePageDecisionNode import SavePageDecisionNode


class MasterPaser:
    """master paser."""

    async def __call__(self, response: Response) -> AsyncGenerator[Any, None]:
        """Parse."""
        engine = ParserDecisionEngine(
            Meta.model_validate(response.meta.get("decision")),
            {
                "NextPageDecisionNode": NextPageDecisionNode(),
                "SavePageDecisionNode": SavePageDecisionNode(),
                "PagingDecisionNode": PagingDecisionNode(),
                "ListPageDecisionNode": ListPageDecisionNode(),
            },
        )
        results = await engine.process(Context(response=response, callback=self.__call__))
        for result in results:
            yield result

"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import AsyncGenerator
from typing import Any

from scrapy.http.response import Response

from crawler.core.Request import Request
from crawler.decisions.pasers.ListPageDecisionNode import ListPageDecisionNode
from crawler.decisions.pasers.NextPageDecisionNode import NextPageDecisionNode
from crawler.decisions.pasers.PagingDecisionNode import PagingDecisionNode
from crawler.decisions.pasers.ParserDecisionEngine import ParserDecisionEngine
from crawler.decisions.pasers.SavePageDecisionNode import SavePageDecisionNode
from crawler.frameworks.scrapy.ScrapyRequestFactory import ScrapyRequestFactory
from crawler.frameworks.scrapy.ScrapyResponse import ScrapyResponse
from crawler.models.dto.Context import Context
from crawler.models.dto.Meta import Meta


class ScrapyPaser:
    """scrapy paser."""

    def __init__(self) -> None:
        """Init."""
        self._rf = ScrapyRequestFactory()
        self._node_map = {
            "NextPageDecisionNode": NextPageDecisionNode(self._rf),
            "SavePageDecisionNode": SavePageDecisionNode(self._rf),
            "PagingDecisionNode": PagingDecisionNode(self._rf),
            "ListPageDecisionNode": ListPageDecisionNode(self._rf),
        }

    async def __call__(self, response: Response) -> AsyncGenerator[Any, None]:
        """Parse."""
        engine = ParserDecisionEngine(
            Meta.model_validate(response.meta.get("decision")),
            self._node_map,
        )
        results = await engine.process(Context(response=ScrapyResponse(response)))
        for result in results:
            if isinstance(result, Request):
                yield await result.revert()
            yield result
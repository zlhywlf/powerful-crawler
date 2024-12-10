"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from scrapy import Request

from crawler.core.DecisionNode import DecisionNode
from crawler.models.Context import Context
from crawler.models.dto.Meta import Meta
from crawler.models.MetaChecker import MetaChecker
from crawler.models.Result import Result


class SavePageDecisionNode(DecisionNode):
    """save page decision node."""

    @override
    async def handle(self, ctx: Context, meta: Meta) -> MetaChecker:
        results: list[Result | Request] = [
            Result(
                id=99,
                type=ctx.response.headers.get("Content-Type", "unknown"),
                content=ctx.response.body,
                name=ctx.response.meta.get("file_name", ""),
            )
        ]
        if ctx.checker:
            results.extend(ctx.checker.result or [])
        return MetaChecker(
            curr_meta=meta,
            type=0,
            result=results,
        )

"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from crawler.core.DecisionNode import DecisionNode
from crawler.core.Request import Request
from crawler.models.dto.Context import Context
from crawler.models.dto.Meta import Meta
from crawler.models.dto.MetaChecker import MetaChecker
from crawler.models.dto.Result import Result


class SavePageDecisionNode(DecisionNode):
    """save page decision node."""

    @override
    async def handle(self, ctx: Context, meta: Meta) -> MetaChecker:
        results: list[Result | Request] = [
            Result(
                id=99,
                type=(await ctx.response.headers).get("Content-Type", "unknown"),
                content=await ctx.response.body,
                name=(await ctx.response.meta).get("file_name", ""),
            )
        ]
        if ctx.checker:
            results.extend(ctx.checker.result or [])
        return MetaChecker(
            curr_meta=meta,
            type=0,
            result=results,
        )
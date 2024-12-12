"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import AsyncGenerator
from typing import override

from crawler.core.DecisionNode import DecisionNode
from crawler.core.Request import Request
from crawler.models.dto.Context import Context
from crawler.models.dto.Result import Result


class SavePageDecisionNode(DecisionNode):
    """save page decision node."""

    @override
    async def handle(self, ctx: Context) -> AsyncGenerator[Result | Request, None]:
        ctx.checker.type = 2
        yield Result(
            id=99,
            type=(await ctx.response.headers).get("Content-Type", "unknown"),
            content=await ctx.response.body,
            name=(await ctx.response.meta).get("file_name", ""),
        )

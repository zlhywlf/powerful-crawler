"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from scrapy import Request

from crawler.core.DecisionNode import DecisionNode
from crawler.models.Context import Context
from crawler.models.Meta import Meta
from crawler.models.MetaChecker import MetaChecker
from crawler.models.Result import Result


class NextPageDecisionNode(DecisionNode):
    """next page decision node."""

    @override
    async def handle(self, ctx: Context, meta: Meta) -> MetaChecker:
        results: list[Result | Request] = [
            Result(id=99, type=ctx.response.headers.get("Content-Type", "unknown"), content=ctx.response.body)
        ]
        if meta.config and meta.config.get("type") == "css":
            if not meta.config.get("needed"):
                results.clear()
            next_pages = ctx.response.css(meta.config.get("next")).extract()
            results.extend([
                ctx.response.follow(
                    next_page, ctx.callback, meta={"decision": meta.meta[0].model_dump()} if meta.meta else None
                )
                for next_page in next_pages
            ])
            return MetaChecker(curr_meta=meta, type=0, result=results)
        return MetaChecker(
            curr_meta=meta,
            type=-1,
            result=results,
        )

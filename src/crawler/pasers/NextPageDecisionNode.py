"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from crawler.core.DecisionNode import DecisionNode
from crawler.models.Context import Context
from crawler.models.Meta import Meta
from crawler.models.MetaChecker import MetaChecker


class NextPageDecisionNode(DecisionNode):
    """next page decision node."""

    @override
    async def handle(self, ctx: Context, meta: Meta) -> MetaChecker:
        t = 0
        if meta.config:
            if meta.config.get("needed"):
                t = 1
            if meta.config.get("type") == "css":
                next_pages = ctx.response.css(meta.config.get("next")).extract()
                return MetaChecker(
                    curr_meta=meta,
                    type=t,
                    result=[
                        ctx.response.follow(
                            next_page,
                            ctx.callback,
                            meta={"decision": meta.model_dump(), "file_name": next_page.replace("/", "_")}
                            if meta.meta
                            else None,
                        )
                        for next_page in next_pages
                    ],
                )
        return MetaChecker(
            curr_meta=meta,
            type=t,
            result=[],
        )

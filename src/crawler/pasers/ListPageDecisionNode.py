"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from crawler.core.DecisionNode import DecisionNode
from crawler.models.Context import Context
from crawler.models.Meta import Meta
from crawler.models.MetaChecker import MetaChecker


class ListPageDecisionNode(DecisionNode):
    """list page decision node."""

    @override
    async def handle(self, ctx: Context, meta: Meta) -> MetaChecker:
        t = 0
        if meta.config:
            if meta.config.get("needed"):
                t = 1
            paths = ctx.response.xpath(meta.config.get("paths")).extract()
            names = ctx.response.xpath(meta.config.get("names")).extract()
            return MetaChecker(
                curr_meta=meta,
                type=t,
                result=[
                    ctx.response.follow(path, meta={"decision": meta.config.get("next"), "file_name": name})
                    for path, name in zip(paths, names, strict=False)
                ],
            )
        return MetaChecker(
            curr_meta=meta,
            type=t,
            result=[],
        )

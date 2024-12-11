"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from crawler.core.DecisionNode import DecisionNode
from crawler.models.dto.Context import Context
from crawler.models.dto.Meta import Meta
from crawler.models.dto.MetaChecker import MetaChecker


class ListPageDecisionNode(DecisionNode):
    """list page decision node."""

    @override
    async def handle(self, ctx: Context, meta: Meta) -> MetaChecker:
        t = 0
        if meta.config:
            if meta.config.get("needed"):
                t = 1
            paths = await ctx.response.extract_by_xpath(str(meta.config.get("paths")))
            names = await ctx.response.extract_by_xpath(str(meta.config.get("names")))
            return MetaChecker(
                curr_meta=meta,
                type=t,
                result=[
                    self.request_factory.create(
                        url=await ctx.response.urljoin(path),
                        meta={**({"decision": meta.meta[0]} if meta.meta else {}), "file_name": name},
                    )
                    for path, name in zip(paths, names, strict=False)
                ],
            )
        return MetaChecker(
            curr_meta=meta,
            type=t,
            result=[],
        )

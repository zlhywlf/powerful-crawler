"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from crawler.core.DecisionNode import DecisionNode
from crawler.models.dto.Context import Context
from crawler.models.dto.Meta import Meta
from crawler.models.dto.MetaChecker import MetaChecker


class NextPageDecisionNode(DecisionNode):
    """next page decision node."""

    @override
    async def handle(self, ctx: Context, meta: Meta) -> MetaChecker:
        t = 0
        if meta.config:
            if meta.config.get("needed"):
                t = 1
            if meta.config.get("type") == "css":
                next_pages = ctx.response.css(meta.config.get("next_path")).extract()
                next_meta = meta.model_copy()
                next_meta.meta.append(meta)
                return MetaChecker(
                    curr_meta=meta,
                    type=t,
                    result=[
                        self.rf.create(
                            url=ctx.response.urljoin(next_page),
                            meta={
                                "decision": next_meta,
                                "file_name": next_page.replace("/", "_"),
                            },
                        )
                        for next_page in next_pages
                    ],
                )
        return MetaChecker(
            curr_meta=meta,
            type=t,
            result=[],
        )

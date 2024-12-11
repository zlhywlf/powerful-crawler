"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from crawler.core.DecisionNode import DecisionNode
from crawler.core.Request import Request
from crawler.models.dto.BaseConfig import BaseConfig
from crawler.models.dto.Context import Context
from crawler.models.dto.Meta import Meta
from crawler.models.dto.MetaChecker import MetaChecker
from crawler.models.dto.Result import Result


class NextPageDecisionNode(DecisionNode):
    """next page decision node."""

    @override
    async def handle(self, ctx: Context, meta: Meta) -> MetaChecker:
        config = NextPageDecisionNode.Config.model_validate_json(meta.config)
        t = 1 if config.needed else 2
        result: list[Result | Request] | None = None
        if config.type == "css":
            next_pages = await ctx.response.extract_by_css(config.next_path)
            next_meta = meta.model_copy(deep=True)
            next_meta.meta.append(meta)
            result = [
                self.request_factory.create(
                    url=await ctx.response.urljoin(next_page),
                    meta={
                        "decision": next_meta,
                        "file_name": next_page.replace("/", "_"),
                    },
                )
                for next_page in next_pages
            ]
        return MetaChecker(
            curr_meta=meta,
            type=t,
            result=result,
        )

    class Config(BaseConfig):
        """config."""

        next_path: str
        type: str

"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import AsyncGenerator
from typing import override

from crawler.core.DecisionNode import DecisionNode
from crawler.core.Request import Request
from crawler.models.dto.BaseConfig import BaseConfig
from crawler.models.dto.Context import Context
from crawler.models.dto.Result import Result


class NextPageDecisionNode(DecisionNode):
    """next page decision node."""

    @override
    async def handle(self, ctx: Context) -> AsyncGenerator[Result | Request, None]:
        meta = ctx.checker.meta
        config = NextPageDecisionNode.Config.model_validate_json(meta.config)
        ctx.checker.type = 1 if config.needed else 2
        if config.type == "css":
            next_pages = await ctx.response.extract_by_css(config.next_path)
            next_meta = meta.model_copy(deep=True)
            next_meta.meta.append(meta)
            for next_page in next_pages:
                yield self.request_factory.create(
                    url=await ctx.response.urljoin(next_page),
                    meta={
                        "decision": next_meta,
                        "file_name": next_page.replace("/", "_"),
                    },
                )

    class Config(BaseConfig):
        """config."""

        next_path: str
        type: str

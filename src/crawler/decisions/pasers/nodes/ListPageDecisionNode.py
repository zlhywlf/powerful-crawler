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


class ListPageDecisionNode(DecisionNode):
    """list page decision node."""

    @override
    async def handle(self, ctx: Context) -> AsyncGenerator[Result | Request, None]:
        meta = ctx.checker.meta
        config = ListPageDecisionNode.Config.model_validate_json(meta.config)
        ctx.checker.type = 1 if config.needed else 2
        paths = await ctx.response.extract_by_xpath(config.paths)
        names = await ctx.response.extract_by_xpath(config.names)
        if paths and names:
            for path, name in zip(paths, names, strict=False):
                yield self.request_factory.create(
                    url=await ctx.response.urljoin(path),
                    meta={**({"decision": meta.meta[0]} if meta.meta else {}), "file_name": name},
                )

    class Config(BaseConfig):
        """config."""

        paths: str
        names: str

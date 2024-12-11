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


class ListPageDecisionNode(DecisionNode):
    """list page decision node."""

    @override
    async def handle(self, ctx: Context, meta: Meta) -> MetaChecker:
        config = ListPageDecisionNode.Config.model_validate_json(meta.config)
        t = 1 if config.needed else 2
        paths = await ctx.response.extract_by_xpath(config.paths)
        names = await ctx.response.extract_by_xpath(config.names)
        result: list[Result | Request] | None = None
        if paths and names:
            result = [
                self.request_factory.create(
                    url=await ctx.response.urljoin(path),
                    meta={**({"decision": meta.meta[0]} if meta.meta else {}), "file_name": name},
                )
                for path, name in zip(paths, names, strict=False)
            ]
        return MetaChecker(
            curr_meta=meta,
            type=t,
            result=result,
        )

    class Config(BaseConfig):
        """config."""

        paths: str
        names: str

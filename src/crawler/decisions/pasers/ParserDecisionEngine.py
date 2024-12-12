"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import AsyncGenerator, Mapping
from typing import override

from crawler.core.DecisionEngine import DecisionEngine
from crawler.core.DecisionNode import DecisionNode
from crawler.core.Request import Request
from crawler.models.dto.Context import Context
from crawler.models.dto.Meta import Meta
from crawler.models.dto.MetaChecker import MetaChecker
from crawler.models.dto.Result import Result


class ParserDecisionEngine(DecisionEngine):
    """paser decision engine."""

    def __init__(self, meta: Meta, node_map: Mapping[str, DecisionNode]) -> None:
        """Init."""
        self._meta = meta
        self._node_map = node_map

    @override
    async def process(self, ctx: Context) -> AsyncGenerator[Result | Request, None]:
        while True:
            surr_meta = ctx.checker.meta
            self._decide(ctx.checker)
            meta = ctx.checker.meta
            if meta is surr_meta or meta.name not in self._node_map:
                break
            node = self._node_map[meta.name]
            async for result in node.handle(ctx):
                yield result

    def _decide(self, checker: MetaChecker) -> None:
        if not self._meta.meta:
            return
        for meta in self._meta.meta:
            if meta.type == checker.type:
                checker.meta = meta
                return

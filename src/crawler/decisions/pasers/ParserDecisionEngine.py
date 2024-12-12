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
        checker = MetaChecker(curr_meta=self._meta, type=self._meta.type)
        while True:
            self._decide(checker)
            meta: Meta | None = checker.next_meta
            if not meta or meta.name not in self._node_map:
                break
            ctx.checker = checker
            node = self._node_map[meta.name]
            checker = await node.handle(ctx, meta)
            if checker.result is None:
                msg = f"process failure for {self._meta}"
                raise RuntimeError(msg)
            for _ in checker.result:
                yield _

    def _decide(self, checker: MetaChecker) -> None:
        if not self._meta.meta:
            return
        for meta in self._meta.meta:
            if meta.type == checker.type:
                checker.next_meta = meta
                return

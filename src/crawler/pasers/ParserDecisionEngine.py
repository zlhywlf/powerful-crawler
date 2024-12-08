"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import Mapping
from typing import override

from scrapy import Request

from crawler.core.DecisionEngine import DecisionEngine
from crawler.core.DecisionNode import DecisionNode
from crawler.models.Context import Context
from crawler.models.Meta import Meta
from crawler.models.MetaChecker import MetaChecker
from crawler.models.Result import Result


class ParserDecisionEngine(DecisionEngine):
    """paser decision engine."""

    def __init__(self, meta: Meta, node_map: Mapping[str, DecisionNode]) -> None:
        """Init."""
        self._meta = meta
        self._node_map = node_map

    @override
    async def process(self, ctx: Context) -> list[Result | Request]:
        meta: Meta | None = self._meta
        result: list[Result | Request] | None = None
        while meta:
            if meta.name not in self._node_map:
                break
            node = self._node_map[meta.name]
            checker = await node.handle(ctx, meta)
            result = checker.result
            self._decide(checker)
            meta = checker.next_meta
            ctx.checker = checker
        if not result:
            msg = f"process failure for {self._meta}"
            raise RuntimeError(msg)
        return result

    def _decide(self, checker: MetaChecker) -> None:
        if not self._meta.meta:
            return
        for meta in self._meta.meta:
            if meta.name != checker.curr_meta.name or not meta.meta:
                continue
            for m in meta.meta:
                if m.type == checker.type:
                    checker.next_meta = m
                    return

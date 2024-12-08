"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import Mapping
from typing import override

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
    async def process(self, ctx: Context) -> list[Result]:
        name: str | None = self._meta.name
        result: list[Result] | None = None
        while name:
            if name not in self._node_map:
                break
            node = self._node_map[name]
            checker = await node.handle(ctx)
            result = checker.result
            self._decide(checker)
            name = checker.next_name
        if not result:
            msg = f"process failure for {self._meta}"
            raise RuntimeError(msg)
        return result

    def _decide(self, checker: MetaChecker) -> None:
        if not self._meta.meta:
            return
        for meta in self._meta.meta:
            if meta.name != checker.curr_name or not meta.meta:
                continue
            for m in meta.meta:
                if m.type == checker.type:
                    checker.next_name = m.name
                    return

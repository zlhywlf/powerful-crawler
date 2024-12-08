"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import override

from crawler.core.DecisionNode import DecisionNode
from crawler.models.Context import Context
from crawler.models.MetaChecker import MetaChecker
from crawler.models.Result import Result


class NextPageDecisionNode(DecisionNode):
    """next page decision node."""

    @override
    async def handle(self, ctx: Context) -> MetaChecker:
        return MetaChecker(
            curr_name="NextPageDecisionNode",
            type=0,
            result=[Result(author=f"author{_}", text=f"text{_}") for _ in range(2)],
        )

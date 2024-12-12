"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from crawler.core.Request import Request
from crawler.models.dto.Context import Context
from crawler.models.dto.Result import Result


class DecisionEngine(ABC):
    """decision engine."""

    @abstractmethod
    async def process(self, ctx: Context) -> AsyncGenerator[Result | Request, None]:
        """Process."""
        yield Result(id=0, name="", type=None, content=None)

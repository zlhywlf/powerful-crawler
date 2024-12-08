"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from scrapy import Request

from crawler.models.Context import Context
from crawler.models.Result import Result


class DecisionEngine(ABC):
    """decision engine."""

    @abstractmethod
    async def process(self, ctx: Context) -> list[Result | Request]:
        """Process."""

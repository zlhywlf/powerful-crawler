"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from crawler.models.Context import Context
from crawler.models.dto.Meta import Meta
from crawler.models.MetaChecker import MetaChecker


class DecisionNode(ABC):
    """decision node."""

    @abstractmethod
    async def handle(self, ctx: Context, meta: Meta) -> MetaChecker:
        """Handle."""

"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod


class DecisionNode(ABC):
    """decision node."""

    @abstractmethod
    async def handle(self) -> None:
        """Handle."""

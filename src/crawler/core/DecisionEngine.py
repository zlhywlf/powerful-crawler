"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod


class DecisionEngine[T](ABC):
    """decision engine."""

    @abstractmethod
    async def process(self) -> T:
        """Process."""

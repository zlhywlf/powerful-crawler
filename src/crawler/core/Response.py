"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod


class Response(ABC):
    """response."""

    @abstractmethod
    async def demo(self) -> None:
        """Demo."""

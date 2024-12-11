"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod


class Request(ABC):
    """request."""

    @abstractmethod
    async def revert(self) -> object:
        """Revert."""

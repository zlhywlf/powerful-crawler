"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod
from typing import Any


class RedisClient(ABC):
    """redis client."""

    @abstractmethod
    async def set(self, name: str, value: str | float) -> None:
        """Set."""

    @abstractmethod
    async def get(self, name: str) -> Any:  # noqa: ANN401
        """Get."""

    @classmethod
    @abstractmethod
    def from_url(cls, url: str, **kwargs: Any) -> "RedisClient":
        """Create instance."""

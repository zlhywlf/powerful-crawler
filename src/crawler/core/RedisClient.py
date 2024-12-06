"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod
from typing import Any, Self

from redis.client import Pipeline


class RedisClient(ABC):
    """redis client."""

    @abstractmethod
    def set(self, name: str, value: str | float) -> None:
        """Set."""

    @abstractmethod
    def get(self, name: str) -> Any:  # noqa: ANN401
        """Get."""

    @classmethod
    @abstractmethod
    def from_url(cls, url: str, **kwargs: Any) -> Self:
        """Create instance."""

    @abstractmethod
    def sadd(self, name: str, value: str | float) -> int:
        """Add to set."""

    @abstractmethod
    def delete(self, name: str) -> None:
        """Delete."""

    @abstractmethod
    def zcard(self, name: str) -> int:
        """Zcard."""

    @abstractmethod
    def execute_command(self, *args: Any, **options: Any) -> None:
        """Execute command."""

    @abstractmethod
    def pipeline(self) -> Pipeline:
        """Pipeline."""

"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod
from typing import Any

from crawler.core.Request import Request


class RequestFactory(ABC):
    """request factory."""

    @abstractmethod
    def create(self, **kwargs: Any) -> Request:
        """Create."""

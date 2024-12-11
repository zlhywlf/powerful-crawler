"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from crawler.core.RequestFactory import RequestFactory
from crawler.models.dto.Context import Context
from crawler.models.dto.Meta import Meta
from crawler.models.dto.MetaChecker import MetaChecker


class DecisionNode(ABC):
    """decision node."""

    def __init__(self, request_factory: RequestFactory) -> None:
        """Init."""
        self._request_factory = request_factory

    @property
    def request_factory(self) -> RequestFactory:
        """Request factory."""
        return self._request_factory

    @abstractmethod
    async def handle(self, ctx: Context, meta: Meta) -> MetaChecker:
        """Handle."""

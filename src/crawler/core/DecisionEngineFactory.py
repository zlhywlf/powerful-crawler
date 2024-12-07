"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from crawler.core.DecisionEngine import DecisionEngine
from crawler.models.Meta import Meta


class DecisionEngineFactory[T](ABC):
    """decision engine factory."""

    @abstractmethod
    def create_engine(self, meta: Meta) -> DecisionEngine[T]:
        """Create engine."""

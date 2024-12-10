"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod

from crawler.core.DecisionEngine import DecisionEngine
from crawler.models.dto.Meta import Meta


class DecisionEngineFactory(ABC):
    """decision engine factory."""

    @abstractmethod
    def create_engine(self, meta: Meta) -> DecisionEngine:
        """Create engine."""

"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from abc import ABC, abstractmethod
from collections.abc import Mapping

from crawler.core.DecisionNode import DecisionNode


class DecisionNodeFactory(ABC):
    """decision node factory."""

    @abstractmethod
    def collect_nodes(self) -> Mapping[str, DecisionNode]:
        """Collect nodes."""

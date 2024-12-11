"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any, override

from crawler.core.Request import Request
from crawler.core.RequestFactory import RequestFactory
from crawler.frameworks.scrapy.ScrapyRequest import ScrapyRequest


class ScrapyRequestFactory(RequestFactory):
    """scrapy request factory."""

    @override
    def create(self, **kwargs: Any) -> Request:
        """Create."""
        return ScrapyRequest(**kwargs)

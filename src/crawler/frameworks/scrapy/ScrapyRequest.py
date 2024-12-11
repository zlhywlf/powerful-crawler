"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any, override

from scrapy import FormRequest

from crawler.core.Request import Request


class ScrapyRequest(Request):
    """scrapy request."""

    def __init__(self, **kwargs: Any) -> None:
        """Init."""
        self._kwargs = kwargs

    @override
    async def revert(self) -> object:
        return FormRequest(**self._kwargs)

"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any, override

from scrapy.http.response import Response as OriginResponse

from crawler.core.Response import Response


class ScrapyResponse(Response):
    """scrapy response."""

    def __init__(self, origin: OriginResponse) -> None:
        """Init."""
        self._origin = origin

    @property
    @override
    async def text(self) -> str:
        return self._origin.text

    @property
    @override
    async def headers(self) -> dict[str, bytes]:
        return self._origin.headers

    @property
    @override
    async def body(self) -> bytes:
        return self._origin.body

    @property
    @override
    async def meta(self) -> dict[str, Any]:
        return self._origin.meta

    @override
    async def urljoin(self, url: str) -> str:
        return self._origin.urljoin(url)

    @override
    async def extract_by_css(self, query: str) -> list[str]:
        return self._origin.css(query).extract()

    @override
    async def extract_by_xpath(self, query: str) -> list[str]:
        return self._origin.xpath(query).extract()

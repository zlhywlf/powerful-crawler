"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import AsyncGenerator
from typing import Any

from scrapy.http.response import Response

from crawler.models.Result import Result


class MasterPaser:
    """master paser."""

    async def __call__(self, response: Response) -> AsyncGenerator[Any, None]:
        """Parse."""
        for quote in response.css("div.quote"):
            yield Result(
                author=quote.xpath("span/small/text()").get(),
                text=quote.css("span.text::text").get(),
            )
        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.__call__)  # type: ignore [arg-type]

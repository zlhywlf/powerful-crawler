"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import Generator
from typing import Any, ClassVar

import scrapy
from scrapy.http.response import Response
from scrapy.settings import _SettingsKeyT


class QuotesSpider(scrapy.Spider):
    """demo."""

    name = "quotes"
    custom_settings: ClassVar[dict[_SettingsKeyT, Any]] = {  # type: ignore [misc]
        "LOG_FORMAT": "%(asctime)s.%(msecs)03d | %(levelname)-8s | %(name)s.%(module)s:%(funcName)s:%(lineno)d - "
        "%(message)s",
    }
    start_urls: ClassVar[list[str]] = [  # type: ignore [misc]
        "https://quotes.toscrape.com/tag/humor/",
    ]

    def parse(self, response: Response) -> Generator[Any, Any, None]:
        """Parse."""
        for quote in response.css("div.quote"):
            yield {
                "author": quote.xpath("span/small/text()").get(),
                "text": quote.css("span.text::text").get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)  # type: ignore [arg-type]

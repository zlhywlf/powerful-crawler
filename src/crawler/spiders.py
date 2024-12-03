"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from collections.abc import Generator
from typing import Any

import scrapy
from scrapy.http.response import Response

g = globals()


class SpiderItem(scrapy.Item):
    """model."""

    author = scrapy.Field()
    text = scrapy.Field()


def parse(obj: scrapy.Spider, response: Response) -> Generator[Any, Any, None]:
    """Parse."""
    for quote in response.css("div.quote"):
        yield SpiderItem(
            author=quote.xpath("span/small/text()").get(),
            text=quote.css("span.text::text").get(),
        )

    next_page = response.css('li.next a::attr("href")').get()
    if next_page is not None:
        yield response.follow(next_page, obj.parse)


def process_item(obj: object, item: SpiderItem, spider: scrapy.Spider) -> SpiderItem:  # noqa: ARG001
    """Process item."""
    spider.log(item)
    return item


_configs = [
    {
        "name": "Quotes",
        "start_urls": [
            "https://quotes.toscrape.com/tag/humor/",
        ],
        "parse": "parse",
        "process_item": "process_item",
    }
]

for config in _configs:
    name = config["name"]
    spider_name = f"{name}Spider"
    pipeliner_name = f"{name}Pipeline"
    parse_func = g[str(config["parse"])]
    process_item_func = g[str(config["process_item"])]
    g.setdefault(
        spider_name,
        type(
            spider_name,
            (scrapy.Spider,),
            {
                "name": name,
                "custom_settings": {
                    "LOG_FORMAT": "%(asctime)s.%(msecs)03d | %(levelname)-8s | "
                    "%(name)s.%(module)s:%(funcName)s:%(lineno)d - %(message)s",
                    "ITEM_PIPELINES": {f"crawler.spiders.{pipeliner_name}": 1},
                },
                "start_urls": config["start_urls"],
                "parse": parse_func,
            },
        ),
    )
    g.setdefault(pipeliner_name, type(pipeliner_name, (), {"process_item": process_item_func}))

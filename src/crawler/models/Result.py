"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

import scrapy


class Result(scrapy.Item):
    """result."""

    author = scrapy.Field()
    text = scrapy.Field()

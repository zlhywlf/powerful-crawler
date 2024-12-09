"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from scrapy.http.response import Response
from sqlmodel import SQLModel

from crawler.models.MetaChecker import MetaChecker


class Context(SQLModel):
    """context."""

    response: Response
    checker: MetaChecker | None = None

    class Config:
        """config."""

        arbitrary_types_allowed = True

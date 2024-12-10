"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from scrapy import Request
from sqlmodel import SQLModel

from crawler.models.dto.Meta import Meta
from crawler.models.Result import Result


class MetaChecker(SQLModel):
    """meta checker."""

    curr_meta: Meta
    type: int
    next_meta: Meta | None = None
    result: list[Result | Request] | None = None

    class Config:
        """config."""

        arbitrary_types_allowed = True

"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel

from crawler.core.Request import Request
from crawler.models.dto.Meta import Meta
from crawler.models.dto.Result import Result


class MetaChecker(BaseModel, arbitrary_types_allowed=True):
    """meta checker."""

    curr_meta: Meta
    type: int
    next_meta: Meta | None = None
    result: list[Result | Request] | None = None

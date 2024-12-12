"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel

from crawler.core.Response import Response
from crawler.models.dto.MetaChecker import MetaChecker


class Context(BaseModel, arbitrary_types_allowed=True):
    """context."""

    response: Response
    checker: MetaChecker

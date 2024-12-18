"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel

from crawler.models.dto.Meta import Meta


class Task(BaseModel):
    """task."""

    id: int
    url: str
    method: str
    meta: Meta

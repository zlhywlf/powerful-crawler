"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any

from pydantic import BaseModel


class Meta(BaseModel):
    """meta."""

    id: int
    name: str
    type: int
    meta: list["Meta"]
    config: dict[str, Any]

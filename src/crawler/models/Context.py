"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any

from sqlmodel import SQLModel


class Context(SQLModel):
    """context."""

    url: str
    meta: dict[str, Any]

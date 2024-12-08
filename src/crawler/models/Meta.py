"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from typing import Any

from sqlalchemy.dialects.sqlite import INTEGER, VARCHAR
from sqlmodel import Column, Field, SQLModel


class Meta(SQLModel):
    """meta."""

    id: int = Field(None, sa_column=Column(INTEGER(), primary_key=True))
    name: str = Field(None, sa_column=Column(VARCHAR()))
    type: int = Field(None, sa_column=Column(INTEGER()))
    meta: list["Meta"] | None = None
    config: dict[str, Any] | None = None

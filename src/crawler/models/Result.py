"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from sqlalchemy.dialects.sqlite import INTEGER, VARCHAR
from sqlmodel import Column, Field, SQLModel


class Result(SQLModel):
    """result."""

    id: int = Field(None, sa_column=Column(INTEGER(), primary_key=True))
    type: str = Field(None, sa_column=Column(VARCHAR()))
    content: bytes = Field(None, sa_column=Column(VARCHAR()))
    name: str = Field(None, sa_column=Column(VARCHAR()))

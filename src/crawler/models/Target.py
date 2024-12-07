"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from sqlalchemy.dialects.sqlite import INTEGER, VARCHAR
from sqlmodel import Column, Field, SQLModel


class Target(SQLModel, table=True):
    """target."""

    id: int = Field(None, sa_column=Column(INTEGER(), primary_key=True))
    url: str = Field(None, sa_column=Column(VARCHAR()))
    method: str = Field(None, sa_column=Column(VARCHAR()))

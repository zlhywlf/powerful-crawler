"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from sqlmodel import SQLModel

from crawler.models.Result import Result


class MetaChecker(SQLModel):
    """meta checker."""

    curr_name: str
    type: int
    next_name: str | None = None
    result: list[Result] | None = None

    class Config:
        """config."""

        arbitrary_types_allowed = True

"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from pydantic import BaseModel


class BaseConfig(BaseModel):
    """base config."""

    needed: bool = False

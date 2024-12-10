"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from sqlalchemy import Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from crawler.models.po.Base import Base


class BaseConfig(Base):
    """base config."""

    __abstract__ = True

    meta_id: Mapped[int] = mapped_column(Integer())
    needed: Mapped[bool] = mapped_column(Boolean(), default=False)

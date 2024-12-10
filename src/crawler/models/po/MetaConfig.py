"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from crawler.models.po.Base import Base


class MetaConfig(Base):
    """meta config."""

    __tablename__ = "meta_config"

    mid: Mapped[int] = mapped_column(ForeignKey("meta.id"))
    name: Mapped[str] = mapped_column(String())
    value: Mapped[str] = mapped_column(String())
    type: Mapped[str] = mapped_column(String())

"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from crawler.models.po.Base import Base
from crawler.models.po.MetaInfo import MetaInfo


class TaskInfo(Base):
    """task info."""

    __tablename__ = "task"

    url: Mapped[str] = mapped_column(String())
    method: Mapped[str] = mapped_column(String())
    meta: Mapped[list[MetaInfo]] = relationship(lazy="immediate")

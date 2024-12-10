"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from crawler.models.po.Base import Base
from crawler.models.po.MetaConfig import MetaConfig


class MetaInfo(Base):
    """meta info."""

    __tablename__ = "meta"

    pid: Mapped[int] = mapped_column(ForeignKey("meta.id"), nullable=True)
    tid: Mapped[int] = mapped_column(ForeignKey("task.id"), nullable=True)
    name: Mapped[str] = mapped_column(String())
    type: Mapped[int] = mapped_column(Integer())
    meta: Mapped[list["MetaInfo"]] = relationship(lazy="immediate")
    config: Mapped[list[MetaConfig]] = relationship(lazy="immediate")

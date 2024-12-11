"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from crawler.models.dto.Meta import Meta
from crawler.models.po.Base import Base


class MetaInfo(Base):
    """meta info."""

    __tablename__ = "meta"

    pid: Mapped[int] = mapped_column(ForeignKey("meta.id"), nullable=True)
    tid: Mapped[int] = mapped_column(ForeignKey("task.id"), nullable=True)
    name: Mapped[str] = mapped_column(String())
    type: Mapped[int] = mapped_column(Integer(), default=0)
    meta: Mapped[list["MetaInfo"]] = relationship(lazy="immediate")
    config: Mapped[str | None] = mapped_column(String(), nullable=True)

    @classmethod
    def load_meta(cls, meta_info: "MetaInfo") -> Meta:
        """Load meta."""
        return Meta(
            id=meta_info.id,
            name=meta_info.name,
            type=meta_info.type,
            meta=[cls.load_meta(_) for _ in meta_info.meta],
            config=meta_info.config or "",
        )

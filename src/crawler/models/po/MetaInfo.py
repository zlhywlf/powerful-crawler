"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from importlib import import_module

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from crawler.models.dto.Meta import Meta
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

    @classmethod
    def load_meta(cls, meta_info: "MetaInfo") -> Meta:
        """Load meta."""

        def to_type(t: str, v: str) -> object:
            """To type."""
            path = f"builtins.{t}"
            dot = path.rindex(".")
            module, name = path[:dot], path[dot + 1 :]
            mod = import_module(module)
            obj = getattr(mod, name)
            return obj(v)

        return Meta(
            id=meta_info.id,
            name=meta_info.name,
            type=meta_info.type,
            meta=[cls.load_meta(_) for _ in meta_info.meta],
            config={_.name: to_type(_.type, _.value) for _ in meta_info.config},
        )

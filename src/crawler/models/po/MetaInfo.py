"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from importlib import import_module
from typing import Any

from sqlalchemy import ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from crawler.models.dto.Meta import Meta
from crawler.models.po.Base import Base


class MetaInfo(Base):
    """meta info."""

    __tablename__ = "meta_info"

    pid: Mapped[int] = mapped_column(ForeignKey("meta_info.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(30))
    type: Mapped[int] = mapped_column(Integer())
    meta: Mapped[list["MetaInfo"]] = relationship()
    config_cls: Mapped[str] = mapped_column(String(30))

    @classmethod
    async def load_meta(cls, session: AsyncSession, id_: int, *, sub: bool = False) -> list[Meta]:
        """Load meta."""
        stmt = select(MetaInfo).where(cls.pid == id_ if sub else cls.id == id_)
        results = (await session.execute(stmt)).scalars()
        if not results:
            return []
        return [
            Meta(
                id=result.id,
                name=result.name,
                type=result.type,
                meta=(await cls.load_meta(session, result.id, sub=True)),
                config=(await cls._load_meta_config(session, result.id, result.config_cls)),
            )
            for result in results
        ]

    @classmethod
    async def _load_meta_config(cls, session: AsyncSession, id_: int, config_cls: str) -> dict[str, Any]:
        """Load meta config."""
        dot = config_cls.rindex(".")
        module, name = config_cls[:dot], config_cls[dot + 1 :]
        mod = import_module(module)
        obj = getattr(mod, name)
        stmt = select(obj).where(obj.meta_id == id_)
        result = (await session.execute(stmt)).scalar()
        return (
            {c.name: getattr(result, c.name, None) for c in result.__table__.columns if c.name not in ["meta_id", "id"]}
            if result
            else {}
        )

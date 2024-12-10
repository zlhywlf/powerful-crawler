"""The asynchronous rpc application.

Copyright (c) 2023-present 善假于PC也 (zlhywlf).
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from crawler.models.po.BaseConfig import BaseConfig


class PagingConfig(BaseConfig):
    """paging config."""

    __tablename__ = "paging_config"

    limit: Mapped[str] = mapped_column(String(30))
    count: Mapped[str] = mapped_column(String(30))
    url: Mapped[str] = mapped_column(String(30))

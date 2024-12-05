from typing import Any

from crawler.congfig import REDIS_CLS
from crawler.core.RedisClient import RedisClient


def get_redis(
    *, url: str = "redis://localhost", redis_cls: type[RedisClient] | None = None, **kwargs: Any
) -> RedisClient:
    """Get redis client."""
    return redis_cls.from_url(url, **kwargs) if redis_cls else REDIS_CLS.from_url(url, **kwargs)

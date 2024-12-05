from typing import Any

from scrapy.settings import BaseSettings
from scrapy.utils.misc import load_object

from crawler.congfig import REDIS_CLS, REDIS_PARAMS
from crawler.core.RedisClient import RedisClient

SETTINGS_PARAMS_MAP = {
    "REDIS_URL": "url",
    "REDIS_HOST": "host",
    "REDIS_PORT": "port",
    "REDIS_DB": "db",
    "REDIS_ENCODING": "encoding",
    "REDIS_DECODE_RESPONSES": "decode_responses",
    "REDIS_CLS": "redis_cls",
}


def get_redis(
    *, url: str = "redis://localhost", redis_cls: type[RedisClient] | None = None, **kwargs: Any
) -> RedisClient:
    """Get redis client."""
    return redis_cls.from_url(url=url, **kwargs) if redis_cls else REDIS_CLS.from_url(url, **kwargs)


def get_redis_from_settings(settings: BaseSettings) -> RedisClient:
    """Get redis client from settings."""
    params = REDIS_PARAMS.copy() | settings.getdict("REDIS_PARAMS")
    for source, dest in SETTINGS_PARAMS_MAP.items():
        val = settings.get(source)
        if val:
            params[dest] = val
    if isinstance(params.get("redis_cls"), str):
        params["redis_cls"] = load_object(params["redis_cls"])
    return get_redis(**params)

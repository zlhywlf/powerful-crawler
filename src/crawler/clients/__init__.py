from typing import Any

from scrapy.settings import BaseSettings
from scrapy.utils.misc import load_object

from crawler.congfig import REDIS_CLS, REDIS_PARAMS
from crawler.core.QueueClient import QueueClient

SETTINGS_PARAMS_MAP = {
    "REDIS_URL": "url",
    "REDIS_HOST": "host",
    "REDIS_PORT": "port",
    "REDIS_DB": "db",
    "REDIS_ENCODING": "encoding",
    "REDIS_DECODE_RESPONSES": "decode_responses",
    "REDIS_CLS": "redis_cls",
}


def get_redis(*, redis_cls: str = REDIS_CLS, url: str = "redis://localhost", **kwargs: Any) -> QueueClient:
    """Get redis client."""
    return load_object(redis_cls).from_url(url=url, **kwargs)  # type: ignore [no-any-return]


def get_redis_from_settings(settings: BaseSettings) -> QueueClient:
    """Get redis client from settings."""
    params = REDIS_PARAMS.copy() | settings.getdict("REDIS_PARAMS")
    for source, dest in SETTINGS_PARAMS_MAP.items():
        val = settings.get(source)
        if val:
            params[dest] = val
    return get_redis(**params)

from crawler.congfig import REDIS_CLS
from crawler.core.RedisClient import RedisClient


def get_redis() -> RedisClient:
    """Get redis client."""
    return REDIS_CLS.from_url()

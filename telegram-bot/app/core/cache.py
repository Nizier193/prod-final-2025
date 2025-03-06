# Redis для кеширования дня

from redis import Redis
from core.config import config

db = Redis(
    host=config.CACHE_HOST,
    port=config.CACHE_PORT
)

def get_cache():
    try:
        yield db
    except Exception:
        db.close()

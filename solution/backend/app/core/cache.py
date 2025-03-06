# Redis для кеширования дня

from redis import Redis
from .config import config

db = Redis(
    host=config.CACHE_HOST,
    port=config.CACHE_PORT
)

# Установка базовых переменных модерации
db.setex(name="moderate", value="True", time=int(10e10))
db.setex(name="moderate_strict", value="False", time=int(10e10))

def get_cache():
    try:
        yield db
    except Exception:
        db.close()

from typing import Optional
from redis import Redis
from core.cache import get_cache

class CacheRepository():
    def __init__(self, cache: Redis) -> None:
        self.cache = cache


    def cache_client_id(self, user_id: str, client_id: str, time: int = 3600) -> bool:
        try:
            self.cache.setex(
                name=user_id,
                value=client_id,
                time=time
            )
            return True
        except Exception as err:
            return False


    def get_cached_client_id(self, user_id: str) -> Optional[str]:
        client_id: bytes = self.cache.getex(name=user_id)
        if not client_id:
            return None

        return client_id.decode()
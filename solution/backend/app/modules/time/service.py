# Бизнес логика

from fastapi import Depends
from redis import Redis
from core.cache import get_cache
from typing import Optional

INF = 10e10 # Чтобы ключик не исчез.

class TimeService():
    time_key_name: str = "time"

    def __init__(self, cache: Redis = Depends(get_cache)) -> None:
        self.cache = cache

        if not self.get_time():
            self.set_time(0) # Если система запустилась только что, ставим тайм 0.


    def get_time(self) -> Optional[int]:
        result: bytes = self.cache.getex(self.time_key_name)
        if not result:
            return None

        return int(result.decode())

    

    def set_time(self, time: int):
        self.cache.setex(
            name=self.time_key_name,
            value=time,
            time=int(+INF)
        )

        return time
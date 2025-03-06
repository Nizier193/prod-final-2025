# Бизнес логика
import re

from redis import Redis
from .repository import BanWordsRepository
from sqlalchemy.orm import Session


class ModerationService():
    def __init__(self, db: Session, cache: Redis) -> None:
        self.repo = BanWordsRepository(db)
        self.cache = cache


    def moderate_naive(self, text: str):
        strict: bytes = self.cache.getex(name="moderate_strict")
        banned_words = self.repo.get_banned_words()

        # Если жёсткая цензура
        if strict.decode() == "True":        
            for word in banned_words:
                if re.search(rf"\b{re.escape(word)}\b", text, flags=re.IGNORECASE):
                    return False, text
            return True, text

        # Цензура мягкая (реплейс на *)
        for word in banned_words:
            text = re.sub(rf"\b{re.escape(word)}\b", "*" * len(word), text, flags=re.IGNORECASE)

        return True, text
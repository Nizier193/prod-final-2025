from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete

from .schemas import banwords_table

class BanWordsRepository:
    def __init__(self, db: Session):
        self.db = db
        banwords_table.metadata.create_all(db.bind)

    def add_banword(self, banword: str) -> bool:
        existing_word = self.db.execute(
            select(banwords_table).where(
                banwords_table.c.banword.ilike(banword)
            )
        ).fetchone()

        if existing_word:
            return False
        
        self.db.execute(insert(banwords_table).values(banword=banword.lower()))
        self.db.commit()
        return True

    def delete_banword(self, banword: str) -> bool:
        result = self.db.execute(
            delete(banwords_table).where(
                banwords_table.c.banword.ilike(banword)
            )
        )
        self.db.commit()
        return result.rowcount > 0


    def get_banned_words(self) -> List[str]:
        banned_words = self.db.execute(
            select(banwords_table.c.banword)
        ).scalars().all()

        if not banned_words:
            return []

        return banned_words
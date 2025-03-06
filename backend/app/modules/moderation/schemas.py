# Модели для БД

from sqlalchemy import MetaData, Table, Column, String
from core.database import get_db
from uuid import uuid4

metadata = MetaData()

banwords_table = Table(
    "banwords",
    metadata,
    Column("id", String, primary_key=True, default=lambda: str(uuid4())),
    Column("banword", String, unique=True, nullable=False),
)

banwords_table.metadata.drop_all(next(get_db()).bind)
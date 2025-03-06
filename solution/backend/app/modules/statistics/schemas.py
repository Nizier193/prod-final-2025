# Модели для БД

from sqlalchemy import Column, Float, Integer, Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class Base(DeclarativeBase):
    pass

# Таблица для кликов
clicked_clients = Table(
    "clicked_clients",
    Base.metadata,
    Column("campaign_id", PG_UUID(as_uuid=True), primary_key=True),
    Column("client_id", PG_UUID(as_uuid=True), primary_key=True),
    Column("cost_per_click", Float),
    Column("date", Integer)
)

# Таблица для просмотров
impression_clients = Table(
    "impression_clients",
    Base.metadata,
    Column("campaign_id", PG_UUID(as_uuid=True), primary_key=True),
    Column("client_id", PG_UUID(as_uuid=True), primary_key=True),
    Column("cost_per_impression", Float),
    Column("date", Integer)
)

from core.database import get_db
clicked_clients.metadata.drop_all(next(get_db()).bind)
impression_clients.metadata.drop_all(next(get_db()).bind)
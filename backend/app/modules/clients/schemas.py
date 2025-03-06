# Модели для БД

from sqlalchemy import MetaData, Table, Column, Integer, String, UUID

metadata = MetaData()

# Таблица клиентов
clients = Table(
    "clients", metadata,
    Column('client_id', UUID, primary_key=True),
    Column('login', String),
    Column('age', Integer),
    Column('location', String),
    Column('gender', String),
    extend_existing=True
)

from core.database import get_db
metadata.drop_all(next(get_db()).bind)
# Модели для БД

from sqlalchemy import Integer, MetaData, Table, Column, String, UUID

metadata_advertisers = MetaData()

# Таблица клиентов
advertisers = Table(
    "advertisers", metadata_advertisers,
    Column('advertiser_id', UUID, primary_key=True),
    Column('name', String),
    extend_existing=True
)


metadata_mlscores = MetaData()

# Таблица млскоров
mlscores = Table(
    "mlscores", metadata_mlscores,
    Column("client_id", UUID, primary_key=True),
    Column("advertiser_id", UUID, primary_key=True),
    Column("score", Integer)
)

from core.database import get_db
metadata_advertisers.drop_all(next(get_db()).bind)
metadata_mlscores.drop_all(next(get_db()).bind)
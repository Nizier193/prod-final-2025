from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import config

client = create_engine(
    url=config.DATABASE_URI
)

SessionLocal = sessionmaker(
    autocommit=False, # Could change this 
    autoflush=False, 
    bind=client
)

# Get database as dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

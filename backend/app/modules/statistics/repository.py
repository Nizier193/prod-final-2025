# Работа с БД

from redis import Redis
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import List, Dict, Optional, Any
from uuid import UUID, uuid4

from core.database import get_db
from core.cache import get_cache
from .schemas import Base, impression_clients, clicked_clients

class StatisticsRepository():
    def __init__(self, db: Session, time_service: Any):
        self.db = db
        self.time_service = time_service
        Base.metadata.create_all(db.bind) # Создание базы


    def add_impression(self, client_id: UUID, campaign_id: UUID, cost_per_impression: float) -> bool:
        impressioned_users = [c.get("client_id") for c in self.get_impressions(campaign_id)]
        if client_id in impressioned_users:
            return False # Не обрабатываем, если такой уже найден

        self.db.execute(
            impression_clients.insert()
            .values(
                client_id=client_id, 
                campaign_id=campaign_id,
                cost_per_impression=cost_per_impression,
                date=self.time_service.get_time()
            )
        )
        self.db.commit()
        return True


    def add_click(self, client_id: UUID, campaign_id: UUID, cost_per_click: float) -> bool:
        clicked_users = [c.get("client_id") for c in self.get_clicks(campaign_id)]
        if client_id in clicked_users:
            return False # Не обрабатываем, если такой уже найден


        self.db.execute(
            clicked_clients.insert()
            .values(
                client_id=client_id,
                campaign_id=campaign_id,
                cost_per_click=cost_per_click,
                date=self.time_service.get_time()
            )
        )
        self.db.commit()
        return True

    def get_impressions(self, campaign_id: UUID, date: Optional[int] = None) -> List[Dict]:
        query = (
            select(impression_clients)
            .where(
                and_(
                    impression_clients.c.campaign_id == campaign_id,
                    (impression_clients.c.date == date) if date else True
                )
            )
        )
        result = self.db.execute(query).mappings().fetchall()
        return [dict(r) for r in result]
    

    def get_clicks(self, campaign_id: UUID, date: Optional[int] = None) -> List[Dict]:
        query = (
            select(clicked_clients)
            .where(
                and_(
                    clicked_clients.c.campaign_id == campaign_id,
                    (clicked_clients.c.date == date) if date else True
                )
            )
        )
        result = self.db.execute(query).mappings().fetchall()
        return [dict(r) for r in result]
    
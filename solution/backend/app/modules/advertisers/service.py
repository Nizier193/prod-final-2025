# Бизнес логика
from uuid import UUID
from .repository import AdvertiserRepository
from .repository import MLScoreRepository
from sqlalchemy.orm import Session


# Сервисный модуль для Dependency Injection
class AdvertiserRepositoryService():
    def __init__(self, db: Session) -> None:
        self.repository = AdvertiserRepository(db)

    def get_advertiser_by_id(self, advertiser_id: UUID):
        return self.repository.get_advertiser_by_id(advertiser_id)
    


# Сервисный модуль для MLScores
class MLScoreRepositoryService():
    def __init__(self, db: Session) -> None:
        self.repository = MLScoreRepository(db)

    def get_mlscores_by_client_id(self, client_id: UUID):
        return self.repository.get_ml_scores_by_client_id(client_id)
    
    def get_mlscore_by_campaign_client_id(self, advertiser_id: UUID, client_id: UUID):
        return self.repository.get_mlscore_by_campaign_client_id(
            advertiser_id=advertiser_id, 
            client_id=client_id
        )
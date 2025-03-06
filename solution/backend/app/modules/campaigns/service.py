# Бизнес логика

from uuid import UUID

from .repository import CampaignRepository
from .models import CampaignCreate
from typing import Any
from sqlalchemy.orm import Session

# Сервисный модуль для Dependency Injection
class CampaignRepositoryService():
    def __init__(self, db: Session) -> None:
        self.repository = CampaignRepository(db)

    def get_campaign_by_id(self, campaign_id: UUID):
        return self.repository.get_campaign_by_id(campaign_id)
    
    def get_campaigns_by_advertiser_id(self, advertiser_id: UUID):
        return self.repository.get_campaigns_by_advertiser_id(advertiser_id)

    def insert_campaign(self, campaign: CampaignCreate):
        return self.repository.insert_campaign(campaign)
    
    def get_campaigns_by_condition(self, client: Any, time: int):
        return self.repository.get_campaigns_by_condition(client, time)

    def update_campaign_text(self, campaignId: UUID, text: str):
        return self.repository.update_campaign_text(campaignId, text)
    
    def get_campaigns(self):
        return self.repository.get_campaigns()
    
    
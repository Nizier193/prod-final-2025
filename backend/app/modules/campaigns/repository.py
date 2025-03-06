# Работа с БД
import pprint
from typing import Any, Dict, List, Optional, cast
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from redis import Redis
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from .schemas import Base
from .schemas import Campaign as CampaignORM
from .schemas import Targeting as TargetingORM
from .models import Campaign, CampaignUpdate

class CampaignRepository():
    def __init__(self, db: Session):
        self.db = db
        Base.metadata.create_all(db.bind) # Создание базы

    
    def get_campaigns(self):
        result = (
            self.db.query(CampaignORM)
            .join(TargetingORM)
            .all()
        )

        return [r.to_dict() for r in result]
    

    def get_campaigns_by_advertiser_id(self, advertiser_id: UUID) -> List[Dict]:
        result = (
            self.db.query(CampaignORM)
            .join(TargetingORM)
            .filter(CampaignORM.advertiser_id == advertiser_id)  # Фильтр по campaigns
            .all()
        )

        return [r.to_dict() for r in result]


    def get_campaign_by_id(self, campaign_id: UUID) -> Optional[Dict]:
        campaign = (
            self.db.query(CampaignORM)
            .join(TargetingORM)
            .filter(CampaignORM.campaign_id == campaign_id)  # Фильтр по campaigns
            .first()
        )

        targeting = (
            self.db.query(TargetingORM)
            .filter(TargetingORM.campaign_id == campaign_id)  # Фильтр по campaigns
            .first()
        )

        if (not campaign) or (not targeting):
            return None
        
        campaign_dict = campaign.to_dict()
        targeting_dict = targeting.to_dict()

        campaign_dict["targeting"] = targeting_dict

        return campaign_dict
    

    def get_campaigns_by_condition(self, client: Any, time: int) -> List[Dict]:
        query = (
            self.db.query(CampaignORM)
            .join(TargetingORM)
            .filter(
                and_(
                    (CampaignORM.start_date <= time) & (time <= CampaignORM.end_date),
                    or_(TargetingORM.age_from.is_(None), TargetingORM.age_from <= client.age),
                    or_(TargetingORM.age_to.is_(None), TargetingORM.age_to >= client.age),
                    or_(TargetingORM.location.is_(None), TargetingORM.location == client.location),
                    
                    # Проверка по гендеру
                    or_(
                        TargetingORM.gender.is_(None),
                        TargetingORM.gender == client.gender.value,
                        TargetingORM.gender == "ALL"
                    )
                )
            )
        )

        result = self.db.execute(query).fetchall()
        dict_result = [campaign[0].to_dict() for campaign in result]

        return dict_result
    
    
    def get_campaigns_with_pagination(self, advertiser_id: UUID, size: int, page: int) -> List[Dict]:
        offset = (page - 1) * size

        campaigns = (
            self.db.query(CampaignORM)
            .filter(CampaignORM.advertiser_id == advertiser_id)
            .offset(offset)
            .limit(size)
            .all()
        )

        return [campaign.to_dict() for campaign in campaigns]

    
    def insert_campaign(self, campaign: Campaign) -> Dict:
        model_dict = campaign.to_dict()
        targeting = model_dict.pop("targeting", {})

        campaign_orm = CampaignORM(**model_dict)
        targeting_orm = TargetingORM(campaign_id=campaign.campaign_id, **targeting)

        self.db.add(campaign_orm)
        self.db.add(targeting_orm)
        self.db.commit()

        return campaign.to_dict()
    

    def delete_campaign(self, campaign_id: UUID) -> None:
        result = (
            self.db.query(CampaignORM)
            .filter(CampaignORM.campaign_id == campaign_id)  # Фильтр по campaigns
            .first()
        )

        self.db.delete(result)
        self.db.commit()


    def update_campaign(self, campaign_id: UUID, updates: CampaignUpdate) -> Dict:
        model_dict = jsonable_encoder(updates.model_dump())
        target_updates = model_dict.pop("targeting", {})

        # Получаем Target и обновляем
        target_orm = (
            self.db.query(TargetingORM)
            .filter(TargetingORM.campaign_id == campaign_id)
            .first()
        )
        for key, value in target_updates.items():
            setattr(target_orm, key, value)

        # Получаем Campaign и обновляем
        campaign_orm = (
            self.db.query(CampaignORM)
            .filter(CampaignORM.campaign_id == campaign_id)
            .first()
        )
        
        # Проверяем на запрещённые поля
        if not (updates.check_restricted_fields(campaign_orm)):
            return False

        for key, value in model_dict.items():
            setattr(campaign_orm, key, value)

        campaign = cast(Dict, self.get_campaign_by_id(campaign_id))
        self.db.commit()

        return campaign


    def update_campaign_text(self, campaign_id: UUID, text: str) -> Dict:
        # Получаем Campaign и обновляе

        campaign_orm = (
            self.db.query(CampaignORM)
            .filter(CampaignORM.campaign_id == campaign_id)
            .first()
        )
        setattr(campaign_orm, "ad_text", text)
        campaign = cast(Dict, self.get_campaign_by_id(campaign_id))

        self.db.commit()
        return campaign

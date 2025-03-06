# Работа с БД
from typing import Dict, List, Optional, Tuple
from uuid import UUID

from sqlalchemy import select

from .schemas import advertisers, metadata_advertisers
from .schemas import mlscores, metadata_mlscores
from .models import Advertiser, MLScore

class AdvertiserRepository():
    def __init__(self, db):
        self.db = db
        metadata_advertisers.create_all(db.bind) # Создание базы


    def get_all_advertiser_ids(self) -> List[UUID]:
        query = select(advertisers)
        result = self.db.execute(query).mappings().fetchall()
        ids = [dict(r).get("advertiser_id") for r in result]

        return ids
    

    def get_advertiser_by_id(self, id: UUID) -> Optional[Dict]:
        query = select(advertisers).where(advertisers.c.advertiser_id == id)
        result = self.db.execute(query).mappings().fetchone()

        if not result:
            return None

        return dict(result)
    

    def insert_advertiser(self, advertiser: Advertiser) -> Dict:
        model_dict = advertiser.model_dump()
        query = advertisers.insert().values(**model_dict)
        self.db.execute(query)
        self.db.commit()

        return model_dict


    def update_advertiser(self, advertiser: Advertiser) -> Dict:
        model_dict = advertiser.model_dump()
        query = (
            advertisers.update()
            .where(advertisers.c.advertiser_id == advertiser.advertiser_id)
            .values(**model_dict)
        )
        self.db.execute(query)
        self.db.commit()
        
        return self.get_advertiser_by_id(advertiser.advertiser_id)

    

class MLScoreRepository():
    def __init__(self, db) -> None:
        self.db = db
        metadata_mlscores.create_all(db.bind)


    def get_all_mlscore_ids(self) -> List[Tuple[UUID, UUID]]:
        query = select(mlscores)
        result = self.db.execute(query).mappings().fetchall()

        return [
            (dict(r).get("client_id"), dict(r).get("advertiser_id")) 
            for r in result
        ]


    def update_mlscore(self, mlscore: MLScore) -> Dict:
        model_dict = mlscore.model_dump()
        query = (
            mlscores.update()
            .where((mlscores.c.client_id == mlscore.client_id) & (mlscores.c.advertiser_id == mlscore.advertiser_id))
            .values(**model_dict)
        )
        self.db.execute(query)
        self.db.commit()

        return model_dict


    def insert_mlscore(self, mlscore: MLScore) -> Dict:
        model_dict = mlscore.model_dump()
        query = mlscores.insert().values(**model_dict)
        self.db.execute(query)
        self.db.commit()

        return model_dict
    

    def get_ml_scores_by_client_id(self, client_id: UUID) -> List[Dict]:
        query = (
            select(mlscores).where(mlscores.c.client_id == client_id)
        )
        result = self.db.execute(query).mappings().fetchall()

        return [dict(r) for r in result]


    def get_mlscore_by_campaign_client_id(self, client_id: UUID, advertiser_id: UUID) -> int:
        query = (
            select(mlscores).where(
                mlscores.c.client_id == client_id,
                mlscores.c.advertiser_id == advertiser_id,
            )
        )
        result = self.db.execute(query).mappings().fetchone()
        if not result:
            return 0

        return dict(result).get("score")

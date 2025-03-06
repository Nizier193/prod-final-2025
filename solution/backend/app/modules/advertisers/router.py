# HTTP

from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from typing import List, Dict
from sqlalchemy.orm import Session
from uuid import UUID

from .repository import AdvertiserRepository, MLScoreRepository
from .models import Advertiser, MLScore
from core.database import get_db
from common.dependencies import get_advertiser_service_repo, get_client_service_repo

router = APIRouter()
mlscore_router = APIRouter()


@router.post("/bulk")
def create_clients(advertisers: List[Advertiser], db: Session = Depends(get_db)):
    repository = AdvertiserRepository(db)

    advertiser_ids = [client.advertiser_id for client in advertisers]
    all_existing_ids = repository.get_all_advertiser_ids()

    result_advertisers: List[Dict] = []
    for advertiser_id, advertiser in zip(advertiser_ids, advertisers):

        if advertiser_id in all_existing_ids:               # Делаем апдейт
            result = repository.update_advertiser(advertiser)
        else:                                           # Добавляем клиента
            result = repository.insert_advertiser(advertiser)

        result_advertisers.append(result)

    return JSONResponse(
        content=jsonable_encoder(result_advertisers),
        status_code=201
    )



@router.get("/{advertiserId}")
def get_client(advertiserId: UUID, db: Session = Depends(get_db)):
    repository = AdvertiserRepository(db)

    advertiser = repository.get_advertiser_by_id(advertiserId)
    
    return JSONResponse(
        content=jsonable_encoder(advertiser),
        status_code=200
    )



@mlscore_router.post("/ml-scores")
def mlscore(
    mlscore: MLScore, 
    db: Session = Depends(get_db),
):
    repository = MLScoreRepository(db)
    client_repo = get_client_service_repo(db)
    advertiser_repo = get_advertiser_service_repo(db)

    if (
        not(client_repo.get_client_by_id(mlscore.client_id)) or
        not(advertiser_repo.get_advertiser_by_id(mlscore.advertiser_id))
    ):
        return JSONResponse(content={"error": "there`s no that client / adv id"}, status_code=404)

    mlscore_id = (mlscore.client_id, mlscore.advertiser_id)
    all_mlscore_ids = repository.get_all_mlscore_ids()

    if mlscore_id in all_mlscore_ids:
        repository.update_mlscore(mlscore)
    else:
        repository.insert_mlscore(mlscore)

    return Response(status_code=200)


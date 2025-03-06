# HTTP

from fastapi import APIRouter, Query, Depends, Response, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import UUID
from redis import Redis

from .models import Ad
from .service import AdProcessor
from core.database import get_db
from core.cache import get_cache
from common.dependencies import (
    get_statistics_service_repo,
    get_campaign_service_repo
)



router = APIRouter()


@router.get("", summary="Получить рекламу на основе параметров клиента.")
def get_ad(
    client_id: UUID = Query(), 
    db: Session = Depends(get_db), 
    cache: Redis = Depends(get_cache)
):
    ad_processor = AdProcessor(db, cache)
    statistics_repo = get_statistics_service_repo(db, cache)

    chosen_campaign = ad_processor.return_campaign(client_id)
    if not chosen_campaign:
        return JSONResponse(content={"status": "No ads available."}, status_code=404)
    
    ad = Ad(ad_id=chosen_campaign.get("campaign_id"), **chosen_campaign)
    status = statistics_repo.add_impression(
        client_id, 
        ad.ad_id, 
        cost_per_impression=chosen_campaign.get("cost_per_impression")
    )
    
    return JSONResponse(
        content=jsonable_encoder(ad),
        status_code=200
    )


@router.post("/{adId}/click")
def click_ad(
    adId: UUID, # equal to campaign_id
    client_id: UUID = Body(..., embed=True),
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    statistics_repo = get_statistics_service_repo(db, cache)
    campaign_repo = get_campaign_service_repo(db)

    campaign = campaign_repo.get_campaign_by_id(adId)
    if not campaign: # Проверка что кампания есть
        return JSONResponse(content={"error": "campaign not found"}, status_code=404)

    # Проверка, можно ли кликнуть.
    click_limit = campaign.get("clicks_limit", 0)
    if len(statistics_repo.get_clicks(adId)) < click_limit:
        status = statistics_repo.add_click(
            client_id=client_id,
            campaign_id=adId,
            cost_per_click=campaign.get("cost_per_click", 0.0)
        )
    else:
        return JSONResponse(status_code=403, content={"error": "Max clicks exceeded."})

    if status: # Если клик зафиксирован
        return Response(status_code=204)
    else: # Если уже был сделан клик
        return JSONResponse(
            content={"status": "already clicked"},
            status_code=200
        )
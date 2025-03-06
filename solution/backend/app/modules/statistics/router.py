# HTTP

from fastapi import APIRouter, Depends
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from redis import Redis
from core.database import get_db
from core.cache import get_cache
from common.dependencies import (
    get_campaign_service_repo,
    get_time_service_repo,
    get_advertiser_service_repo
)
from .service import StatisticsCalcService
from .repository import StatisticsRepository

from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/campaigns/{campaignId}")
def get_campaign_stat(campaignId: UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    time_service = get_time_service_repo(cache) # Модуль для управления временем
    statistics_repo = StatisticsRepository(db, time_service) # Модуль для работы с сохранённой статистикой
    campaign_repo = get_campaign_service_repo(db) # Модуль для работы с кампаниями

    if not campaign_repo.get_campaign_by_id(campaignId):
        return JSONResponse(content={"error": "there`s no that campaignId"}, status_code=404)

    statistics = StatisticsCalcService(statistics_repo, campaign_repo) # Модуль для расчёта статистик
    stats_by_campaign = statistics.get_campaign_stats(campaignId)

    return JSONResponse(
        content=jsonable_encoder(stats_by_campaign),
        status_code=200
    )


@router.get("/advertisers/{advertiserId}/campaigns")
def get_advertiser_stat(advertiserId: UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    time_service = get_time_service_repo(cache) # Модуль для управления временем
    statistics_repo = StatisticsRepository(db, time_service) # Модуль для работы с сохранённой статистикой
    campaign_repo = get_campaign_service_repo(db) # Модуль для работы с кампаниями
    advertiser_repo = get_advertiser_service_repo(db)

    if not advertiser_repo.get_advertiser_by_id(advertiserId):
        return JSONResponse(content={"error": "there`s no that advertiserId"}, status_code=404)

    statistics = StatisticsCalcService(statistics_repo, campaign_repo) # Модуль для расчёта статистик
    stats_by_advertiser = statistics.get_advertiser_stats(advertiserId)

    return JSONResponse(
        content=jsonable_encoder(stats_by_advertiser),
        status_code=200
    )


@router.get("/campaigns/{campaignId}/daily")
def get_campaign_stat_daily(campaignId: UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    time_service = get_time_service_repo(cache) # Модуль для управления временем
    statistics_repo = StatisticsRepository(db, time_service) # Модуль для работы с сохранённой статистикой
    campaign_repo = get_campaign_service_repo(db) # Модуль для работы с кампаниями

    if not campaign_repo.get_campaign_by_id(campaignId):
        return JSONResponse(content={"error": "there`s no that campaignId"}, status_code=404)

    statistics = StatisticsCalcService(statistics_repo, campaign_repo) # Модуль для расчёта статистик
    stats_by_campaign_daily = statistics.get_campaign_stats_daily(campaignId, to_day=time_service.get_time())

    return JSONResponse(
        content=jsonable_encoder(stats_by_campaign_daily),
        status_code=200
    )


@router.get("/advertisers/{advertiserId}/campaigns/daily")
def get_advertiser_stat_daily(advertiserId: UUID, db: Session = Depends(get_db), cache: Redis = Depends(get_cache)):
    time_service = get_time_service_repo(cache) # Модуль для управления временем
    statistics_repo = StatisticsRepository(db, time_service) # Модуль для работы с сохранённой статистикой
    campaign_repo = get_campaign_service_repo(db) # Модуль для работы с кампаниями
    advertiser_repo = get_advertiser_service_repo(db)

    if not advertiser_repo.get_advertiser_by_id(advertiserId):
        return JSONResponse(content={"error": "there`s no that advertiserId"}, status_code=404)

    statistics = StatisticsCalcService(statistics_repo, campaign_repo) # Модуль для расчёта статистик
    stats_by_campaign_daily = statistics.get_advertiser_stats_daily(advertiserId, to_day=time_service.get_time())

    return JSONResponse(
        content=jsonable_encoder(stats_by_campaign_daily),
        status_code=200
    )
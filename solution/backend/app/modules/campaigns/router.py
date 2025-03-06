# HTTP

from fastapi import APIRouter, Depends, Query, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from redis import Redis
from sqlalchemy.orm import Session
from uuid import UUID, uuid4

from core.config import config
from core.cache import get_cache
from core.database import get_db
from common.dependencies import (
    get_advertiser_service_repo, 
    get_openrouter, 
    get_moderation_service_repo,
    OpenRouterIntegration, 
    OpenRouterRequest,
)

from .repository import CampaignRepository
from .models import Campaign, CampaignCreate, CampaignUpdate


router = APIRouter()

@router.get("/{campaignId}/advertiser")
def get_advertiser_by_campaign_id(
    campaignId: UUID,
    db: Session = Depends(get_db),
):
    repository = CampaignRepository(db)
    adv_repo = get_advertiser_service_repo(db)

    campaign = repository.get_campaign_by_id(campaignId)
    if not campaign:
        return JSONResponse(
            content={"error": "campaign not found"}, 
            status_code=404
        )
    
    campaign_id = campaign.get("advertiser_id", "")
    advertiser = adv_repo.get_advertiser_by_id(campaign_id)

    return JSONResponse(
        content=jsonable_encoder(advertiser), 
        status_code=200
    )


@router.post("/{advertiserId}/campaigns")
def create_campaign(
    advertiserId: UUID, 
    campaign_create: CampaignCreate, 
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    repository = CampaignRepository(db)
    adv_repo = get_advertiser_service_repo(db)
    moderator = get_moderation_service_repo(db, cache)

    advertiser = adv_repo.get_advertiser_by_id(advertiserId)
    if not advertiser:
        return JSONResponse(
            content={"error": "there`s no that advertiserId"}, 
            status_code=404
        )

    campaign = Campaign(
        campaign_id=uuid4(),
        advertiser_id=advertiserId,
        **campaign_create.model_dump()
    )

    # Модерация
    moderate: bytes = cache.getex("moderate")
    if moderate.decode() == "True":
        if not campaign.moderate_text(moderator=moderator):
            return JSONResponse(
                status_code=400, 
                content={"error": "Your text is against rules."}
            )

    result = repository.insert_campaign(campaign)

    return JSONResponse(
        content=jsonable_encoder(result),
        status_code=201
    )



@router.get("/{advertiserId}/campaigns")
def get_campaigns_with_pagination(
    advertiserId: UUID,
    size: int = Query(default=10e10, gt=0),
    page: int = Query(default=1, gt=0),
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    repository = CampaignRepository(db)
    adv_repo = get_advertiser_service_repo(db)

    advertiser = adv_repo.get_advertiser_by_id(advertiserId)
    if not advertiser:
        return JSONResponse(
            content={"error": "there`s no that advertiserId"}, 
            status_code=404
        )
    
    result = repository.get_campaigns_with_pagination(
        advertiserId,
        size=size,
        page=page
    )

    return JSONResponse(
        content=jsonable_encoder(result),
        status_code=200
    )


@router.get("/{advertiserId}/campaigns/{campaignId}")
def get_campaign_by_id(
    advertiserId: UUID,
    campaignId: UUID,
    db: Session = Depends(get_db),
):
    repository = CampaignRepository(db)
    adv_repo = get_advertiser_service_repo(db)

    advertiser = adv_repo.get_advertiser_by_id(advertiserId)
    if not advertiser:
        return JSONResponse(
            content={"error": "there`s no that advertiserId"}, 
            status_code=404
        )
    
    campaign = repository.get_campaign_by_id(campaignId)
    if not campaign:
        return JSONResponse(
            content={"error": "campaign not found"}, 
            status_code=404
        )
    elif campaign.get("advertiser_id") != advertiserId:
        return JSONResponse(
            content={"error": "you have no access to this campaign"}, 
            status_code=403
        )
    
    return JSONResponse(
        content=jsonable_encoder(campaign),
        status_code=200
    )


@router.put("/{advertiserId}/campaigns/{campaignId}")
def update_campaign_by_id(
    advertiserId: UUID,
    campaignId: UUID,
    model_update: CampaignUpdate,
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    repository = CampaignRepository(db)
    adv_repo = get_advertiser_service_repo(db)
    moderator = get_moderation_service_repo(db, cache)

    advertiser = adv_repo.get_advertiser_by_id(advertiserId)
    if not advertiser:
        return JSONResponse(
            content={"error": "there`s no that advertiserId"}, 
            status_code=404
        )
    
    campaign = repository.get_campaign_by_id(campaignId)
    if not campaign:
        return JSONResponse(
            content={"error": "campaign not found"}, 
            status_code=404
        )
    elif campaign.get("advertiser_id") != advertiserId:
        return JSONResponse(
            content={"error": "you have no access to this campaign"}, 
            status_code=403
        )
    
    # Модерация
    moderate: bytes = cache.getex("moderate")
    if moderate.decode() == "True":
        if not model_update.moderate_text(moderator=moderator):
            return JSONResponse(
                status_code=400, 
                content={"error": "Your text is against rules."}
            )

    # Проверка на изменение запрещенных полей
    result = repository.update_campaign(campaignId, model_update)
    if not result:
        return JSONResponse(
            content={"error": "You can`t modify these fields."},
            status_code=400
        )

    return JSONResponse(
        content=jsonable_encoder(result),
        status_code=200
    )


@router.delete("/{advertiserId}/campaigns/{campaignId}")
def delete_campaign_by_id(
    advertiserId: UUID,
    campaignId: UUID,
    db: Session = Depends(get_db)
):
    repository = CampaignRepository(db)
    adv_repo = get_advertiser_service_repo(db)

    advertiser = adv_repo.get_advertiser_by_id(advertiserId)
    if not advertiser:
        return JSONResponse(content={"error": "there`s no that advertiserId"}, status_code=404)
    
    campaign = repository.get_campaign_by_id(campaignId)
    if not campaign:
        return JSONResponse(content={"error": "campaign not found"}, status_code=404)
    elif campaign.get("advertiser_id") != advertiserId:
        return JSONResponse(content={"error": "you have no access to this campaign"}, status_code=403)
    
    repository.delete_campaign(campaignId)
    
    return Response(status_code=204)


@router.post("/{advertiserId}/campaigns/{campaignId}/generate-ad-text")
async def generate_ad_text(
    advertiserId: UUID,
    campaignId: UUID,
    prompt: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache),
    openrouter: OpenRouterIntegration = Depends(get_openrouter),
):
    # Инициализация репозиториев
    campaign_repo = CampaignRepository(db)
    adv_repo = get_advertiser_service_repo(db)
    moderator = get_moderation_service_repo(db, cache)

    # Получение данных о кампании и рекламодателе
    campaign = campaign_repo.get_campaign_by_id(campaignId)
    if not campaign:
        return JSONResponse(status_code=404, content="Campaign not found")

    advertiser = adv_repo.get_advertiser_by_id(advertiserId)
    if not advertiser:
        return JSONResponse(status_code=404, content="Advertiser not found")

    campaign_targeting = campaign.get("targeting", {})
    targeting_description = "; ".join(
        f"{key} {value}"
        for key, value in {
            "Люди от": campaign_targeting.get("age_from"),
            "Люди до": campaign_targeting.get("age_to"),
            "Люди пола": campaign_targeting.get("gender"),
            "Люди в месте": campaign_targeting.get("location"),
        }.items()
        if value
    )

    full_prompt = (
        f"Сгенерируй рекламный текст по желанию заказчика: {prompt}; "
        f"Название рекламы: {campaign.get('ad_title')}; "
        f"На кого реклама нацелена: {targeting_description};"
    )

    # Генерация текста через LLM
    request = OpenRouterRequest(prompt=full_prompt, model=config.OPENROUTER_MODEL)
    llm_response = await openrouter.generate_response(request)
    if llm_response.status != "success":
        return JSONResponse(
            content={"error": "failed to generate text", "detail": llm_response.response},
            status_code=404
        )

    # Обновление текста кампании
    updated_campaign = campaign_repo.update_campaign_text(campaignId, llm_response.response)


    moderate: bytes = cache.getex("moderate")
    campaign = Campaign.model_validate(updated_campaign)

    # Модерируем сгенерированный контент
    if moderate.decode() == "True":
        if not campaign.moderate_text(moderator=moderator):
            return JSONResponse(status_code=400, content={"error": "Your text is against the rules."})

    return JSONResponse(
        content=jsonable_encoder(campaign),
        status_code=200,
    )

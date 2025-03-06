from fastapi import Depends
from redis import Redis
from sqlalchemy.orm import Session

from llm.integration import OpenRouterIntegration, OpenRouterRequest
from modules.clients.service import ClientRepositoryService
from modules.campaigns.service import CampaignRepositoryService
from modules.advertisers.service import AdvertiserRepositoryService
from modules.advertisers.service import MLScoreRepositoryService
from modules.time.service import TimeService
from modules.statistics.service import StatisticsRepositoryService
from modules.moderation.service import ModerationService

from core.config import config
from core.database import get_db
from core.cache import get_cache

# Returns ClientRepositoryService
def get_client_service_repo(db: Session = Depends(get_db)):
    return ClientRepositoryService(db)


# Returns CampaignRepositoryService
def get_campaign_service_repo(db: Session = Depends(get_db)):
    return CampaignRepositoryService(db)


# Returns AdvertiserRepositoryService
def get_advertiser_service_repo(db: Session = Depends(get_db)):
    return AdvertiserRepositoryService(db)


# Returns MLScoreRepositoryService
def get_mlscore_service_repo(db: Session = Depends(get_db)):
    return MLScoreRepositoryService(db)


# Returns TimeService
def get_time_service_repo(cache: Redis = Depends(get_cache)):
    return TimeService(cache)


# Returns StatisticsRepositoryService
def get_statistics_service_repo(
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_cache)
    ):
    time_service = get_time_service_repo(cache)

    return StatisticsRepositoryService(db, time_service)


# llm integration
def get_openrouter():
    return OpenRouterIntegration(
        api_key=config.OPENAI_API_KEY,
        base_url=config.OPENAI_BASEURL
    )

# moderation
def get_moderation_service_repo(
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_cache)
    ):
    return ModerationService(db, cache)

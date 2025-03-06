# Бизнес логика
from typing import Dict, List

from .models import DailyStats, Stats
from .repository import StatisticsRepository
from uuid import UUID

from sqlalchemy.orm import Session

from common.dependencies import CampaignRepositoryService
from common.dependencies import TimeService


# Сервисный модуль для использования в других модулях
class StatisticsRepositoryService():
    def __init__(self, db: Session, time_service: TimeService) -> None:
        self.repository = StatisticsRepository(db, time_service)

    def get_clicks(self, campaign_id: UUID):
        return self.repository.get_clicks(campaign_id)

    
    def get_impressions(self, campaign_id: UUID):
        return self.repository.get_impressions(campaign_id)
    
    
    def add_impression(self, 
            client_id: UUID, 
            campaign_id: UUID, 
            cost_per_impression: float) -> bool:
        return self.repository.add_impression(client_id, campaign_id, cost_per_impression)
    

    def add_click(self, 
            client_id: UUID, 
            campaign_id: UUID, 
            cost_per_click: float) -> bool:
        return self.repository.add_click(client_id, campaign_id, cost_per_click)
    


class StatisticsCalcService():
    def __init__(self, repository: StatisticsRepository, campaign_repo: CampaignRepositoryService) -> None:
        self.repository = repository
        self.campaign_repo = campaign_repo


    def get_campaign_stats(self, campaignId: UUID) -> Stats:
        # Получение общей статистики по одной рекламной кампании

        impression_stats = self.repository.get_impressions(campaignId)
        click_stats = self.repository.get_clicks(campaignId)

        stats = self.calc_stats(impression_stats, click_stats)
        return stats
    

    def get_advertiser_stats(self, advertiserId: UUID) -> Stats:
        campaigns = self.campaign_repo.get_campaigns_by_advertiser_id(advertiserId)

        stats = Stats() # type: ignore # Пустая статистика до заполнения
        for campaign in campaigns:
            campaign_id = campaign.get("campaign_id", "")
            impression_stats = self.repository.get_impressions(campaign_id)
            click_stats = self.repository.get_clicks(campaign_id)

            # Сложение со статистиками других кампаний
            stats += self.calc_stats(impression_stats, click_stats)

        return stats
    

    def get_campaign_stats_daily(self, campaignId: UUID, to_day: int) -> List[DailyStats]:
        daily_stats: List[DailyStats] = []

        for day in range(1, to_day + 1):
            impression_stats = self.repository.get_impressions(campaignId, day)
            click_stats = self.repository.get_clicks(campaignId, day)

            stats = self.calc_stats(impression_stats, click_stats).model_dump()
            stats["date"] = day

            daily_stat = DailyStats.model_validate(stats)
            daily_stats.append(daily_stat)
        
        return daily_stats
    

    def get_advertiser_stats_daily(self, advertiserId: UUID, to_day: int) -> List[DailyStats]:
        campaigns = self.campaign_repo.get_campaigns_by_advertiser_id(advertiserId)
        daily_stats: List[DailyStats] = []


        for day in range(1, to_day + 1):
            stats = Stats() # type: ignore

            for campaign in campaigns:
                campaign_id = campaign.get("campaign_id", "")
                impression_stats = self.repository.get_impressions(campaign_id, day)
                click_stats = self.repository.get_clicks(campaign_id, day)

                # Сложение со статистиками дня
                stats += self.calc_stats(impression_stats, click_stats)


            stats = stats.model_dump()
            stats["date"] = day

            daily_stat = DailyStats.model_validate(stats)
            daily_stats.append(daily_stat)

        return daily_stats
    

    @staticmethod
    def calc_stats(impression_stats: List[Dict], click_stats: List[Dict]) -> Stats:
        if impression_stats:
            impression_sum = sum([r.get("cost_per_impression") for r in impression_stats]) # type: ignore
        else:
            impression_sum = 0

        if click_stats:
            click_sum = sum([r.get("cost_per_click") for r in click_stats]) # type: ignore
        else:
            click_sum = 0


        stats = Stats(
            impressions_count=len(impression_stats),
            clicks_count=len(click_stats),
            spent_impressions=impression_sum,
            spent_clicks=click_sum,
        ) # type: ignore

        return stats

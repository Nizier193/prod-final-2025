# Бизнес логика
from typing import Dict, List, Optional
from uuid import UUID

from random import choice

from common.dependencies import (
    ClientRepositoryService, get_client_service_repo,
    CampaignRepositoryService, get_campaign_service_repo,
    MLScoreRepositoryService, get_mlscore_service_repo,
    TimeService, get_time_service_repo,
    StatisticsRepositoryService, get_statistics_service_repo
)


# Класс, отвечающий за определение релевантной рекламы.
class AdProcessor():
    def __init__(self, db, cache, default_ctr: float = 0.01):
        self.campaign_repo = get_campaign_service_repo(db)
        self.client_repo = get_client_service_repo(db)
        self.mlscore_repo = get_mlscore_service_repo(db)
        self.time_repo = get_time_service_repo(cache)
        self.stat_repo = get_statistics_service_repo(db, cache)

        self.default_ctr = default_ctr
    

    def return_campaign(self, client_id: UUID):
        client = self.client_repo.get_client_by_id(client_id)
        campaigns = self.campaign_repo.get_campaigns_by_condition(client, self.time_repo.get_time())

        # Обработка каждой кампании
        filtered_campaigns: List[Dict] = []
        for campaign in campaigns:
            campaign_id = campaign.get("campaign_id")
            
            campaign_impressions = self.stat_repo.get_impressions(campaign_id)
            client_impression_ids = [str(d.get("client_id")) for d in campaign_impressions]

            if str(client_id) in client_impression_ids:
                continue # Пропускаем, т.к. уже показывали рекламу

            if len(campaign_impressions) < campaign.get("impressions_limit", 0):
                # Добавляем ключи для дальнейшей обработки
                campaign["current_impressions"] = len(campaign_impressions)
                campaign["current_clicks"] = len(self.stat_repo.get_clicks(campaign_id))
                campaign["score"] = self.mlscore_repo.get_mlscore_by_campaign_client_id(
                    advertiser_id=campaign.get("advertiser_id"),
                    client_id=client_id
                )

                filtered_campaigns.append(campaign)
        
        max_score = -float('inf')
        selected_ad = None
        
        for ad in filtered_campaigns:
            current_impressions = ad.get('current_impressions', 0)
            current_clicks = ad.get('current_clicks', 0)
            
            # Расчет CTR
            if current_impressions > 0:
                ctr = current_clicks / current_impressions
            else:
                ctr = self.default_ctr
            
            # Прибыль платформы
            expected_profit = ad['cost_per_impression'] + ad['cost_per_click'] * ctr
            profit_component = expected_profit * 0.5
            
            # Релевантность
            relevance_component = ad['score'] * 0.25
            
            # Выполнение лимитов
            new_imp = current_impressions + 1
            max_imp = ad['impressions_limit']
            completion_imp = min(new_imp / max_imp, 1.0)

            completion_clicks = current_clicks / ad['clicks_limit']
            
            compliances = []
            compliances.append(completion_imp)
            compliances.append(completion_clicks)
            
            avg_completion = sum(compliances) / len(compliances)
            compliance_component = avg_completion * 0.15
            compliance_component = 0.15  # Нет лимитов
        
            # Скорость
            speed_component = 0.1
            
            total_before_penalty = profit_component + relevance_component + compliance_component + speed_component
            
            # Штраф за превышение лимитов показов
            penalty = 0.0
            if 'max_impressions' in ad:
                max_imp = ad['max_impressions']
                new_imp = current_impressions + 1
                if new_imp > max_imp:
                    excess = new_imp - max_imp
                    percent_over = (excess / max_imp) * 100
                    num_penalties = int(percent_over // 5)
                    penalty = num_penalties * 0.05
            
            total_score = total_before_penalty * (1 - penalty)
            
            if total_score > max_score:
                max_score = total_score
                selected_ad = ad

        return selected_ad


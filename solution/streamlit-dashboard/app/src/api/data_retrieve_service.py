from typing import Dict, List, Optional, Tuple
from uuid import UUID
import requests
import pandas as pd
from random import choice

from src.api.data_seed import (
    make_clients,
    make_advertisers,
    make_campaign_on_server,
    set_time,
    make_view,
    make_click
)

class DataRetrieveService:
    """
    Сервис для работы с данными рекламных кампаний и статистикой
    """
    
    def __init__(self, config) -> None:
        self.base_url = config.BACKEND_BASEURL + "/"
        self.stats_endpoint = self.base_url + "/stats"

    def insert_some_data(
        self, 
        n_clients: int, 
        n_advertisers: int, 
        n_campaigns_per_advertiser: int, 
        max_impressions: int, 
        max_clicks: int
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Генерирует тестовые данные для рекламных кампаний
        
        Args:
            n_clients: количество клиентов
            n_advertisers: количество рекламодателей
            n_campaigns_per_advertiser: количество кампаний на рекламодателя
            max_impressions: максимальное количество показов
            max_clicks: максимальное количество кликов
            
        Returns:
            DataFrame с данными о кампаниях и рекламодателях
        """
        # Создаем клиентов и рекламодателей
        client_ids, _ = make_clients(self.base_url, n_clients)
        advertisers = make_advertisers(self.base_url, n_advertisers)

        # Создаем кампании для каждого рекламодателя
        campaigns_data = self._generate_campaigns(
            advertisers,
            n_campaigns_per_advertiser,
            max_impressions,
            max_clicks
        )

        # Генерируем активность пользователей
        self._generate_user_activity(client_ids)

        return pd.DataFrame(campaigns_data), pd.DataFrame({"Client IDs": client_ids})

    def _generate_campaigns(
        self,
        advertisers: List,
        n_campaigns: int,
        max_impressions: int,
        max_clicks: int
    ) -> List[Dict]:
        """Создает рекламные кампании для рекламодателей"""
        campaigns_advertisers = []
        
        for advertiser in advertisers:
            campaign_ids, _ = make_campaign_on_server(
                self.base_url,
                advertiser,
                n_campaigns,
                max_impressions,
                max_clicks
            )
            
            campaigns_advertisers.extend([
                {
                    "advertiser_id": advertiser,
                    "campaign_id": campaign_id
                }
                for campaign_id in campaign_ids
            ])
            
        return campaigns_advertisers

    def _generate_user_activity(self, client_ids: List) -> None:
        """Генерирует пользовательскую активность (просмотры и клики)"""
        current_day = 1
        
        for idx, client in enumerate(client_ids):
            set_time(self.base_url, current_day)
            
            # Генерируем просмотр
            ad, status_code = make_view(self.base_url, client)

            # Генерируем клик с вероятностью 50%
            if choice([True, False]):
                # Только если пользователь посмотрел рекламу - кликаем
                if status_code == 200:
                    make_click(self.base_url, ad.get("ad_id"), client)

            if idx in [2 ** i for i in range(50)]:
                current_day += 1

    def get_campaign_stat(self, campaign_id: str) -> Optional[Dict]:
        """Получает статистику по конкретной кампании"""
        endpoint = f"{self.stats_endpoint}/campaigns/{campaign_id}"
        return self._make_request(endpoint)

    def get_advertiser_stat(self, advertiser_id: str) -> Optional[Dict]:
        """Получает статистику по всем кампаниям рекламодателя"""
        endpoint = f"{self.stats_endpoint}/advertisers/{advertiser_id}/campaigns"
        return self._make_request(endpoint)

    def get_campaign_stat_daily(self, campaign_id: str) -> Optional[pd.DataFrame]:
        """Получает ежедневную статистику по кампании"""
        endpoint = f"{self.stats_endpoint}/campaigns/{campaign_id}/daily"
        return self._make_request_to_df(endpoint)

    def get_advertiser_stat_daily(self, advertiser_id: str) -> Optional[pd.DataFrame]:
        """Получает ежедневную статистику по всем кампаниям рекламодателя"""
        endpoint = f"{self.stats_endpoint}/advertisers/{advertiser_id}/campaigns/daily"
        return self._make_request_to_df(endpoint)

    def _make_request(self, endpoint: str) -> Optional[Dict]:
        """Выполняет GET-запрос и возвращает результат в виде словаря"""
        response = requests.get(url=endpoint)
        return response.json() if response.status_code == 200 else None

    def _make_request_to_df(self, endpoint: str) -> Optional[pd.DataFrame]:
        """Выполняет GET-запрос и возвращает результат в виде DataFrame"""
        response = requests.get(url=endpoint)
        if response.status_code != 200 or not response.json():
            return None
        return pd.DataFrame(response.json())

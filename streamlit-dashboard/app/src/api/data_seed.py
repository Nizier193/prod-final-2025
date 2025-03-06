from src.models.schemas import *

import requests
from random import randint, choice
from typing import Tuple, List, Dict
from uuid import uuid4, UUID
from string import ascii_uppercase

class CampaignGenerator:
    """Генератор данных для рекламных кампаний"""
    
    LOCATIONS = ["STREAMLIT_LOCATION"] # Для того чтобы выборка не пересекалась с реальными данными
    GENDERS = ["MALE"]
    
    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """Генерирует случайную строку из заглавных букв"""
        return ''.join(choice(ascii_uppercase) for _ in range(length))

    @classmethod
    def create_targeting(cls) -> Targeting:
        """Создает объект таргетинга с случайными параметрами"""
        return Targeting(
            gender=choice(cls.GENDERS),
            age_from=0,
            age_to=100,
            location=choice(cls.LOCATIONS)
        )

    @classmethod
    def create_campaign(cls, max_impressions: int, max_clicks: int) -> CampaignCreate:
        """Создает объект кампании с заданными ограничениями"""
        return CampaignCreate(
            impressions_limit=max_impressions,
            clicks_limit=max_clicks,
            cost_per_impression=randint(0, 1000),
            cost_per_click=randint(0, 500),
            ad_title=cls.generate_random_string(),
            ad_text=cls.generate_random_string(),
            start_date=0,
            end_date=100,
            targeting=cls.create_targeting()
        )

class APIClient:
    """Клиент для работы с API"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Выполняет HTTP-запрос"""
        url = f"{self.base_url}{endpoint}"
        return requests.request(method, url, **kwargs)

    def create_campaign(
        self, 
        advertiser_id: str, 
        num: int,
        max_impressions: int,
        max_clicks: int
    ) -> Tuple[List[str], List[Campaign]]:
        """Создает заданное количество кампаний для рекламодателя"""
        endpoint = f"advertisers/{advertiser_id}/campaigns"
        campaigns = []
        campaign_ids = []

        for _ in range(num):
            campaign = CampaignGenerator.create_campaign(max_impressions, max_clicks).model_dump()
            campaign["targeting"]["gender"] = "ALL"

            response = self._make_request("POST", endpoint, json=campaign)
            campaign_id = response.json().get("campaign_id")
            campaign_ids.append(campaign_id)

            campaigns.append({
                "advertiser_id": advertiser_id,
                "campaign_id": campaign_id,
                **campaign
            })

        return campaign_ids, [Campaign.model_validate(campaign) for campaign in campaigns]

    def get_campaign(self, advertiser_id: str, campaign_id: str) -> Campaign:
        """Получает информацию о кампании"""
        endpoint = f"advertisers/{advertiser_id}/campaigns/{campaign_id}"
        response = self._make_request("GET", endpoint)
        return Campaign(**response.json())

    def create_clients(self, num: int) -> Tuple[List[str], List[Dict]]:
        """Создает заданное количество клиентов"""
        clients = [
            {
                "client_id": str(uuid4()),
                "login": CampaignGenerator.generate_random_string(),
                "age": 50,
                "location": choice(CampaignGenerator.LOCATIONS),
                "gender": choice(["MALE"])
            }
            for _ in range(num)
        ]

        self._make_request("POST", "clients/bulk", json=clients)
        return [x.get("client_id") for x in clients], clients

    def create_advertisers(self, num: int) -> List[str]:
        """Создает заданное количество рекламодателей"""
        advertisers = [
            {
                "advertiser_id": str(uuid4()),
                "name": CampaignGenerator.generate_random_string(),
            }
            for _ in range(num)
        ]

        self._make_request("POST", "advertisers/bulk", json=advertisers)
        return [x.get("advertiser_id") for x in advertisers]

    def create_view(self, user_id: str) -> Tuple[Dict, int]:
        """Создает просмотр рекламы"""
        response = self._make_request("GET", "ads", params={"client_id": user_id})
        return response.json(), response.status_code

    def create_click(self, ad_id: str, user_id: str) -> int:
        """Регистрирует клик по рекламе"""
        response = self._make_request(
            "POST",
            f"ads/{ad_id}/click",
            json={"client_id": user_id}
        )
        return response.status_code

    def set_time(self, time: int) -> None:
        """Устанавливает текущее время"""
        response = self._make_request(
            "POST",
            "time/advance",
            json={"current_date": time}
        )
        assert response.status_code == 200

# Для обратной совместимости создаем функции-обертки
def make_campaign(max_impressions: int, max_clicks: int) -> CampaignCreate:
    return CampaignGenerator.create_campaign(max_impressions, max_clicks)

def make_campaign_on_server(baseurl: str, *args, **kwargs) -> Tuple[List[str], List[Campaign]]:
    return APIClient(baseurl).create_campaign(*args, **kwargs)

def get_campaign_from_server(baseurl: str, advertiser_id: str, campaign_id: str) -> Campaign:
    return APIClient(baseurl).get_campaign(advertiser_id, campaign_id)

def make_clients(baseurl: str, num: int) -> Tuple[List[str], List[Dict]]:
    return APIClient(baseurl).create_clients(num)

def make_advertisers(baseurl: str, num: int) -> List[str]:
    return APIClient(baseurl).create_advertisers(num)

def make_view(baseurl: str, user_id: str) -> Tuple[Dict, int]:
    return APIClient(baseurl).create_view(user_id)

def make_click(baseurl: str, ad_id: str, user_id: str) -> int:
    return APIClient(baseurl).create_click(ad_id, user_id)

def set_time(baseurl: str, time: int) -> None:
    APIClient(baseurl).set_time(time)

from typing import Dict, List, Optional
import requests
from requests import Response

from core.config import config

class APIService():
    def __init__(self) -> None:
        self.baseurl = config.BACKEND_BASEURL.rstrip("/")


    def get_ad(self, clientId: str) -> requests.Response:
        """Получение рекламы по айди клиента."""
        response = requests.get(
            self.baseurl + "/ads",
            params={"client_id": clientId}
        )
        
        return response
    
    def click_ad(self, clientId: str, adId: str) -> Response:
        response = requests.post(
            self.baseurl + "/ads/{adId}/click".format(adId=adId),
            json={"client_id": clientId}
        )
        return response # По статус коду понимаем какой статус клика.
    
    def get_campaign(self, advertiserId: str, campaignId: str) -> Response:
        """Получение рекламной кампании по её ID"""
        response = requests.get(
            (self.baseurl + "/advertisers/{advertiserId}/campaigns/{campaignId}")
            .format(advertiserId=advertiserId, campaignId=campaignId)
        )
        return response
    
    def get_advertiser(self, advertiserId: str) -> Response:
        """Получение рекламодателя по его ID"""
        response = requests.get(
            (self.baseurl + "/advertisers/{advertiserId}").format(advertiserId=advertiserId)
        )
        return response
    
    def get_advertiser_by_campaign_id(self, campaignId: str) -> Response:
        """Получение рекламодателя по кампании, которая ему принадлежит."""
        response = requests.get(
            (self.baseurl + "/advertisers/{campaignId}/advertiser").format(campaignId=campaignId)
        )
        return response
    
    def get_images(self, campaignId: str) -> Response:
        """Получение всех картинок рекламы по ID"""
        response = requests.get(
            self.baseurl +  "/images/{campaignId}".format(campaignId=campaignId)
        )
        return response
    
    def get_time(self) -> Response:
        response = requests.get(
            self.baseurl + "/time"
        )
        return response
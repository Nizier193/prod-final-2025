from typing import Dict, List
import requests


class APIRegistryClient:
    """Клиент для работы с API"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Выполняет HTTP-запрос"""
        url = f"{self.base_url}{endpoint}"
        return requests.request(method, url, **kwargs)
    
    def create_clients_bulk(self, clients: List[Dict]) -> requests.Response:
        response = self._make_request("POST", "/clients/bulk", json=clients)
        return response
    
    def create_advertisers_bulk(self, advertisers: List[Dict]) -> requests.Response:
        response = self._make_request("POST", "/advertisers/bulk", json=advertisers)
        return response
    
    def create_campaign(self, advertiserId: str, campaign: Dict) -> requests.Response:
        response = self._make_request("POST", f"/advertisers/{advertiserId}/campaigns", json=campaign)
        return response
    
    def generate_text(self, prompt: str, advertiserId: str, campaignId: str):
        response = self._make_request(
            "POST", 
            f"/advertisers/{advertiserId}/campaigns/{campaignId}/generate-ad-text",
            json={"prompt": prompt}
        )
        return response
    
    def set_time(self, time: int) -> requests.Response:
        response = self._make_request("POST", f"/time/advance", json={"current_date": time})
        return response
    
    def get_time(self) -> int:
        response = self._make_request("GET", f"/time")
        return response.json().get("current_date")

    def moderation_switch(self, status: bool) -> requests.Response:
        response = self._make_request("POST", f"/moderation/active", json={"status": status})
        return response
    
    def moderation_strict(self, status: bool) -> requests.Response:
        response = self._make_request("POST", f"/moderation/strict", json={"status": status})
        return response
    
    def moderation_get_banwords(self) -> requests.Response:
        response = self._make_request("GET", f"/moderation/banwords")
        return response
    
    def moderation_add_banwords(self, banword: str) -> requests.Response:
        response = self._make_request("POST", f"/moderation/banwords", json={"banword": banword})
        return response
    
    def get_ad(self, clientId: str) -> requests.Response:
        response = self._make_request("GET", f"/ads", params={"client_id": clientId})
        return response
    
    def make_click(self, adId: str, clientId: str) -> requests.Response:
        response = self._make_request("POST", f"/ads/{adId}/click", json={"client_id": clientId})
        return response
    
    def add_photo(self, campaignId: str, image):
        response = self._make_request("POST", f"/images/{campaignId}", files={"image": image})
        return response
    
    def get_photos(self, campaignId: str):
        response = self._make_request("GET", f"/images/{campaignId}")
        return response

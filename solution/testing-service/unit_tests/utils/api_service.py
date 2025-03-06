from core.config import config
from typing import List, Dict, Tuple

import requests

baseurl = config.BACKEND_BASEURL

class BackendAPIService():
    def __init__(self) -> None:
        self.base_url = config.BACKEND_BASEURL.rstrip("/")

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Выполняет HTTP-запрос"""
        url = f"{self.base_url}{endpoint}"
        return requests.request(method, url, **kwargs)
    
    def create_clients_bulk(self, clients: List[Dict], expected_status: int) -> Tuple[requests.Response, bool]:
        response = self._make_request("POST", "/clients/bulk", json=clients)
        return response, response.status_code == expected_status
    
    def create_advertisers_bulk(self, advertisers: List[Dict], expected_status: int) -> Tuple[requests.Response, bool]:
        response = self._make_request("POST", "/advertisers/bulk", json=advertisers)
        return response, response.status_code == expected_status
    
    def create_mlscore(self, mlscore: Dict, expected_status: int) -> Tuple[requests.Response, bool]:
        response = self._make_request("POST", "/advertisers/bulk", json=mlscore)
        return response, response.status_code == expected_status
    
    def create_campaign(self, advertiserId: str, campaign: Dict, expected_status: int) -> Tuple[requests.Response, bool]:
        response = self._make_request("POST", f"/advertisers/{advertiserId}/campaigns", json=campaign)
        return response, response.status_code == expected_status
    
    def put_campaign(self, advertiserId: str, campaignId: str, campaignPut: Dict, expected_status: int) -> Tuple[requests.Response, bool]:
        response = self._make_request("PUT", f"/advertisers/{advertiserId}/campaigns/{campaignId}", json=campaignPut)
        return response, response.status_code == expected_status
    
    def delete_campaign(self, advertiserId: str, campaignId: str, expected_status: int) -> Tuple[requests.Response, bool]:
        response = self._make_request("DELETE", f"/advertisers/{advertiserId}/campaigns/{campaignId}")
        return response, response.status_code == expected_status
    
    def moderation_switch(self, status: bool, expected_status: int) -> Tuple[requests.Response, bool]:
        response = self._make_request("POST", f"/moderation/active", json={"status": status})
        return response, response.status_code == expected_status
    
    def moderation_strict(self, status: bool, expected_status: int) -> Tuple[requests.Response, bool]:
        response = self._make_request("POST", f"/moderation/strict", json={"status": status})
        return response, response.status_code == expected_status
    
    def moderation_get_banwords(self, expected_status: int) -> Tuple[requests.Response, bool]:
        response = self._make_request("GET", f"/moderation/banwords")
        return response, response.status_code == expected_status
    
    def moderation_add_banwords(self, banword: str, expected_status: int) -> Tuple[requests.Response, bool]:
        response = self._make_request("POST", f"/moderation/banwords", json={"banword": banword})
        return response, response.status_code == expected_status
    
    def set_time(self, time: int, expected_status: int) -> Tuple[requests.Response, bool]:
        response = self._make_request("POST", f"/time/advance", json={"current_date": time})
        return response, response.status_code == expected_status
    
    def get_time(self, expected_status: int) -> Tuple[int, bool]:
        response = self._make_request("GET", f"/time")
        return response.json().get("current_date"), response.status_code == expected_status
    
    def generate_text(self, prompt: str, advertiserId: str, campaignId: str, expected_status: int) -> Tuple[requests.Response, bool]:
        response = self._make_request(
            "POST", 
            f"/advertisers/{advertiserId}/campaigns/{campaignId}/generate-ad-text",
            json={"prompt": prompt}
        )
        return response, response.status_code == expected_status
    
    def get_ad(self, clientId: str, expected_status: int) -> Tuple[requests.Response, bool]:
        response = self._make_request("GET", f"/ads", params={"client_id": clientId})
        return response, response.status_code == expected_status
    
    def make_click(self, adId: str, clientId: str, expected_status: int) -> Tuple[requests.Response, bool]:
        response = self._make_request("POST", f"/ads/{adId}/click", json={"client_id": clientId})
        return response, response.status_code == expected_status
    
    def add_photo(self, campaignId: str, image, expected_status: int) -> Tuple[requests.Response, bool]:
        response = self._make_request("POST", f"/images/{campaignId}", files={"image": image})
        return response, response.status_code == expected_status
    
    def get_photos(self, campaignId: str, expected_status: int) -> Tuple[requests.Response, bool]:
        response = self._make_request("GET", f"/images/{campaignId}")
        return response, response.status_code == expected_status
    


def delete_campaign(campaign_id, advertiser_id):
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns/{campaignId}"

    response = requests.delete(
        url.format(advertiserId=advertiser_id, campaignId=campaign_id)
    )
    print(response.content)
    assert response.status_code == 204



from typing import List, Optional
from src.api.api_service import APIService
from src.models.schemas import ViewAdResponse, ClickAdResponse


class ClientAPIService():
    def __init__(self) -> None:
        self.api_service = APIService()

    def client_view_ad(self, clientId: str) -> Optional[ViewAdResponse]:
        ad = self.api_service.get_ad(clientId) # Здесь идёт начисление рекламки.
        if (ad.status_code != 200):
            return None
        
        ad_json = ad.json()

        # Получение рекламодателя
        advertiser = self.api_service.get_advertiser(ad_json.get("advertiser_id", ""))
        if advertiser.status_code != 200:
            return None
        
        advertiser_json = advertiser.json()

        return ViewAdResponse(
            ad_id=ad_json.get("ad_id"),
            advertiser_name=advertiser_json.get("name"),
            ad_title=ad_json.get("ad_title"),
            ad_text=ad_json.get("ad_text"),
        )
    

    def client_click_ad(self, clientId: str, adId: str) -> Optional[ClickAdResponse]:
        # Получение рекламодателя
        current_time = self.api_service.get_time()
        click = self.api_service.click_ad(clientId, adId)

        advertiser = self.api_service.get_advertiser_by_campaign_id(adId)
        if (
            (advertiser.status_code != 200) or 
            (current_time.status_code != 200) or 
            (click.status_code not in [200, 204])
        ):
            return None
        
        advertiser_json = advertiser.json()

        # Получение картинок рекламы
        campaign = self.api_service.get_campaign(
            advertiserId=advertiser_json.get("advertiser_id"),
            campaignId=adId
        ).json()
        campaign_images: List[str] = self.api_service.get_images(campaign.get("campaign_id")).json()

        # Вычисление остатка действия рекламы
        remains_active = "Срок рекламы неограничен."
        campaign_end_date = campaign.get("end_date", None)
        if campaign_end_date:
            remains_active = (campaign_end_date - current_time.json().get("current_date"))

        return ClickAdResponse(
            ad_id=campaign.get("campaign_id"),
            advertiser_name=advertiser_json.get("name"),
            ad_title=campaign.get("ad_title"),
            ad_text=campaign.get("ad_text"),
            remains_active=remains_active,
            image_urls=[img.get("url") for img in campaign_images]
        )
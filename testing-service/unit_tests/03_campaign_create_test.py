from core.config import config

from uuid import uuid4
import requests

from utils.data_service import (
    make_advertisers,
    make_campaign
)
from utils.api_service import delete_campaign

baseurl = config.BACKEND_BASEURL

def test_creating_normal_campaigns():
    """Нормальная кампания"""
    advertisers = make_advertisers(10)
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns"

    campaign = make_campaign()

    for advertiser in advertisers:
        response = requests.post(
            url.format(advertiserId=advertiser),
            json=campaign.model_dump()
        )
        assert response.status_code == 201

        # Удаляем кампанию, чтобы не мешать другим тестам
        campaign_id = response.json().get("campaign_id")
        delete_campaign(campaign_id, advertiser)


def test_creating_broken_campaigns():
    """Тест некорректных кампаний списком"""

    advertisers = make_advertisers(10)
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns"

    fine_campaign = make_campaign().model_dump()

    incorrect_age_to = fine_campaign.copy()
    incorrect_age_to["targeting"]["age_to"] = "20" # age_to - строка

    incorrect_cost_per_impression = fine_campaign.copy()
    incorrect_cost_per_impression["cost_per_impression"] = "20" # cost_per_impression - строка

    incorrect_gender = fine_campaign.copy()
    incorrect_gender["targeting"]["gender"] = "BINARY" # нет такого пола

    broken = [incorrect_age_to, incorrect_cost_per_impression, incorrect_gender]

    advertiser = advertisers[0]
    for broke in broken:
        response = requests.post(
            url.format(advertiserId=advertiser),
            json=broke
        )
        assert response.status_code == 400
    

def test_advertiser_not_found():
    """Тест рекламодателя нет"""
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns"
    advertiser = str(uuid4())

    campaign = make_campaign()

    response = requests.post(
        url.format(advertiserId=advertiser),
        json=campaign.model_dump()
    )

    assert response.status_code == 404



from core.config import config

import requests

from utils.data_service import (
    make_advertisers,
    make_campaign_on_server,
    make_campaign_put,
    get_campaign_from_server
)
from utils.api_service import delete_campaign

baseurl = config.BACKEND_BASEURL


def test_campaign_put_normal():
    advertiser = make_advertisers(1)[0]
    campaign_ids, campaigns = make_campaign_on_server(advertiser, 1)

    campaign_id, campaign = campaign_ids[0], campaigns[0]
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns/{campaignId}"

    new_title = "Some Updated Title"
    new_text = "Some Updated Text"

    campaign_put = make_campaign_put().model_dump()
    campaign_put["ad_title"] = new_title
    campaign_put["ad_text"] = new_text

    response = requests.put(
        url.format(advertiserId=advertiser, campaignId=campaign_id),
        json=campaign_put
    )

    print(campaign)
    print(campaign_put)
    assert response.status_code == 200

    campaign_json = response.json()
    assert (campaign_json.get("ad_title") == new_title) and (campaign_json.get("ad_text") == new_text) # Новые поля сменились

    campaign, status_code = get_campaign_from_server(advertiser, campaign_id)
    assert (campaign.ad_title == new_title) and (campaign.ad_text == new_text)

    delete_campaign(campaign.campaign_id, advertiser)


def test_campaign_put_broken():
    advertiser = make_advertisers(1)[0]
    campaign_ids, campaigns = make_campaign_on_server(advertiser, 1)

    campaign_id, campaign = campaign_ids[0], campaigns[0]
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns/{campaignId}"

    campaign_put = make_campaign_put().model_dump()
    campaign_put["ad_title"] = None
    campaign_put["ad_text"] = None
    campaign_put["start_date"] = None # Такого быть не может

    response = requests.put(
        url.format(advertiserId=advertiser, campaignId=campaign_id),
        json=campaign_put
    )

    assert response.status_code == 400

    delete_campaign(campaign_id, advertiser)


def test_campaign_put_all_fields():
    # Даты и лимиты
    advertiser = make_advertisers(1)[0]
    campaign_ids, campaigns = make_campaign_on_server(advertiser, 1)

    campaign_id, campaign = campaign_ids[0], campaigns[0]
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns/{campaignId}"

    campaign_put = make_campaign_put().model_dump()
    
    campaign_put["ad_title"] = "Хороший текст"
    campaign_put["ad_text"] = "Прекрасный текст"
    campaign_put["cost_per_click"] = 70
    campaign_put["cost_per_impression"] = 10
    
    campaign_put["targeting"]["location"] = "Moscow"
    campaign_put["targeting"]["gender"] = None
    campaign_put["targeting"]["age_from"] = 50
    campaign_put["targeting"]["age_to"] = 70

    response = requests.put(
        url.format(advertiserId=advertiser, campaignId=campaign_id),
        json=campaign_put
    )

    print(response.json())
    assert response.status_code == 200

    delete_campaign(campaign_id, advertiser)


def test_campaign_put_restricted_fields():
    # Даты и лимиты
    advertiser = make_advertisers(1)[0]
    campaign_ids, campaigns = make_campaign_on_server(advertiser, 1)

    campaign_id, campaign = campaign_ids[0], campaigns[0]
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns/{campaignId}"

    campaign_put = make_campaign_put().model_dump()
    campaign_put["start_date"] = 50
    campaign_put["end_date"] = 80
    campaign_put["impressions_limit"] = 70    
    campaign_put["clicks_limit"] = 70

    campaign_put["ad_title"] = "Хороший текст"
    campaign_put["ad_text"] = "Прекрасный текст"
    campaign_put["cost_per_click"] = 70
    campaign_put["cost_per_impression"] = 10
    
    campaign_put["targeting"]["location"] = "Moscow"
    campaign_put["targeting"]["gender"] = None
    campaign_put["targeting"]["age_from"] = 50
    campaign_put["targeting"]["age_to"] = 70

    response = requests.put(
        url.format(advertiserId=advertiser, campaignId=campaign_id),
        json=campaign_put
    )

    assert response.status_code == 400

    delete_campaign(campaign_id, advertiser)
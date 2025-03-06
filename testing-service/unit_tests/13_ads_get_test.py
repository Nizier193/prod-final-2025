from core.config import config

from typing import List
from utils.api_service import delete_campaign, BackendAPIService
from utils.data_service import (
    make_campaign_on_server,
    make_clients,
    make_advertisers
)

service = BackendAPIService()

from fixtures.ads_fixtures import (
    campaigns_empty_target,
    campaigns_age_target,
    campaign_gender_target,
    campaign_location_target,
)

def test_target_null(campaigns_empty_target):
    client = make_clients(num=1, age=15, location="MOSCOW")[0]
    advertiser = make_advertisers(1)[0]

    time, status = service.set_time(15, 200)
    assert status

    campaign_ids: List[str] = []
    for campaign in campaigns_empty_target:
        response, status = service.create_campaign(
            advertiserId=advertiser, 
            campaign=campaign,
            expected_status=201
        )
        assert status

        campaign_json = response.json()
        campaign_ids.append(campaign_json.get("campaign_id"))

    # 5 раз получаем кампании
    retrieved_campaign_ids: List[str] = []
    for _ in range(5):    
        response, status = service.get_ad(client, expected_status=200)
        assert status

        ad_json = response.json()
        retrieved_campaign_ids.append(ad_json.get('ad_id'))

    assert sorted(campaign_ids) == sorted(retrieved_campaign_ids)

    # Удаляем, чтобы не пересекаться с другими тестами
    for campaign_id in campaign_ids:
        delete_campaign(campaign_id, advertiser)


def test_campaign_age_target(campaigns_age_target):
    low_age_client = make_clients(1, age=5)[0]
    medium_age_client = make_clients(1, age=15)[0]
    high_age_client = make_clients(1, age=75)[0]

    clients = [low_age_client, medium_age_client, high_age_client]
    advertiser = make_advertisers(1)[0]

    campaign_ids: List[str] = []
    for campaign in campaigns_age_target:
        response, status = service.create_campaign(
            advertiserId=advertiser,
            campaign=campaign,
            expected_status=201
        )
        assert status

        campaign_json = response.json()
        campaign_ids.append(campaign_json.get("campaign_id"))

        # В порядке low_age, medium_age, high_age

    for client_id, campaign_id in zip(clients, campaign_ids):
        ad, status = service.get_ad(client_id, expected_status=200)
        
        assert status
        ad_json = ad.json()

        assert ad_json.get("ad_id") == campaign_id

    
    for id in campaign_ids:
        delete_campaign(id, advertiser)


def test_location_target(campaign_gender_target):
    kazan_client = make_clients(1, location="kazan")[0]
    msk_client = make_clients(1, location="msk")[0]
    spb_client = make_clients(1, location="spb")[0]
    taiga_client = make_clients(1, location="taiga")[0]

    advertiser = make_advertisers(1)[0]

    clients = [kazan_client, msk_client, spb_client, taiga_client]

    campaign_ids: List[str] = []
    for campaign in campaign_gender_target[0]:
        response, status = service.create_campaign(
            advertiserId=advertiser,
            campaign=campaign,
            expected_status=201
        )
        assert status

        campaign_json = response.json()
        campaign_ids.append(campaign_json.get("campaign_id"))

        # В порядке создания

    for client_id, campaign_id in zip(clients, campaign_ids):
        ad, status = service.get_ad(client_id, expected_status=200)
        
        assert status
        ad_json = ad.json()

        assert ad_json.get("ad_id") == campaign_id

    for id in campaign_ids:
        delete_campaign(id, advertiser)


def test_gender_target(campaign_gender_target):
    male_client = make_clients(1, gender="MALE")[0]
    female_client = make_clients(1, gender="FEMALE")[0]

    advertiser = make_advertisers(1)[0]

    campaign_ids: List[str] = []
    for campaign in campaign_gender_target[0]:
        response, status = service.create_campaign(
            advertiserId=advertiser,
            campaign=campaign,
            expected_status=201
        )
        assert status

        campaign_json = response.json()
        campaign_ids.append(campaign_json.get("campaign_id"))

        # В порядке создания

    male_campaigns, female_campaigns = campaign_ids[:5], campaign_ids[5:]

    for campaign_id in male_campaigns:
        ad, status = service.get_ad(male_client, expected_status=200)
        
        assert status
        ad_json = ad.json()

        assert ad_json.get("ad_id") == campaign_id

    for campaign_id in female_campaigns:
        ad, status = service.get_ad(female_client, expected_status=200)
        
        assert status
        ad_json = ad.json()

        assert ad_json.get("ad_id") == campaign_id

    for id in campaign_ids:
        delete_campaign(id, advertiser)
from core.config import config

from uuid import uuid4
import requests

from utils.data_service import (
    make_advertisers,
    make_campaign_on_server,
)
from utils.api_service import delete_campaign

baseurl = config.BACKEND_BASEURL

def test_get_campaign():
    advertiser = make_advertisers(1)[0]
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns/{campaignId}"

    ids, campaigns = make_campaign_on_server(advertiser, 10)

    for id, campaign in zip(ids, campaigns):
        response = requests.get(
            url.format(advertiserId=advertiser, campaignId=id)
        )
        assert response.status_code == 200
        assert campaign == response.json()

        delete_campaign(id, advertiser)


def test_get_campaign_pagination():
    advertiser = make_advertisers(1)[0]
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns"

    ids, campaigns = make_campaign_on_server(advertiser, 10)

    for id, campaign in zip(ids, campaigns):
        response = requests.get(
            url.format(advertiserId=advertiser),
            params={
                "page": 1,
                "size": 2
            }
        )
        assert response.status_code == 200
        assert len(response.json()) == 2

    for id in ids:
        delete_campaign(id, advertiser)


def test_get_no_campaign():
    advertiser = make_advertisers(1)[0]
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns/{campaignId}"

    real_ids, campaigns = make_campaign_on_server(advertiser, 10)
    fake_ids = [str(uuid4()) for _ in range(10)]

    for id, campaign in zip(fake_ids, campaigns):
        response = requests.get(
            url.format(advertiserId=advertiser, campaignId=id)
        )
        assert response.status_code == 404

    
    for id in real_ids:
        delete_campaign(id, advertiser)
        

def test_get_no_access_to_campaign():
    advertiser = make_advertisers(1)[0]
    other_advertiser = make_advertisers(1)[0]
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns/{campaignId}"

    ids, campaigns = make_campaign_on_server(advertiser, 10)

    for id, campaign in zip(ids, campaigns):
        response = requests.get(
            url.format(advertiserId=other_advertiser, campaignId=id)
        )
        assert response.status_code == 403

        delete_campaign(id, advertiser)
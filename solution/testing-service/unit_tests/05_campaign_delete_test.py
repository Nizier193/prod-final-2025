from core.config import config

import requests
from utils.data_service import (
    make_campaign_on_server,
    make_advertisers,
    get_campaign_from_server
)

baseurl = config.BACKEND_BASEURL

def test_delete_campaign():
    advertiser = make_advertisers(1)[0]
    campaign_ids, campaigns = make_campaign_on_server(advertiser, 1)

    campaign_id, campaign = campaign_ids[0], campaigns[0]
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns/{campaignId}"

    response = requests.delete(
        url.format(advertiserId=advertiser, campaignId=campaign_id)
    )
    assert (response.status_code == 204) # Удалили

    campaign, status_code = get_campaign_from_server(advertiser, campaign_id)
    assert (status_code == 404) # Такой кампании не найдено


def test_delete_no_access():
    advertisers = make_advertisers(2)
    advertiser, other_advertiser = advertisers
    campaign_ids, campaigns = make_campaign_on_server(advertiser, 1)

    campaign_id, campaign = campaign_ids[0], campaigns[0]
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns/{campaignId}"

    response = requests.delete(
        url.format(advertiserId=other_advertiser, campaignId=campaign_id)
    )
    assert (response.status_code == 403) # Нельзя удалить

    campaign, status_code = get_campaign_from_server(advertiser, campaign_id)
    assert (status_code == 200) # кампания есть

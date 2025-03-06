from core.config import config

from pathlib import Path
import requests

from utils.data_service import (
    make_advertisers,
    make_campaign
)
from utils.api_service import delete_campaign

baseurl = config.BACKEND_BASEURL
basepath = Path(config.PATH_TO_SOURCES)

def test_making_ml_text():
    advertisers = make_advertisers(1)[0]
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns"

    campaign = make_campaign()

    response = requests.post(
        url.format(advertiserId=advertisers),
        json=campaign.model_dump()
    )
    assert response.status_code == 201

    campaignId=response.json().get("campaign_id")

    response = requests.post(
        url = (baseurl + "/advertisers/{advertiserId}" + "/campaigns/{campaignId}/generate-ad-text").format(advertiserId=advertisers, campaignId=campaignId),
        json={"prompt": "Красивый текст."}
    )
    print(response.json())
    assert response.status_code == 200

    delete_campaign(response.json().get("campaign_id"), advertisers)

from core.config import config

import requests
from uuid import uuid4, UUID
from typing import List, Dict, Optional, Tuple
from random import choice, randint

from models.campaign_models import (
    Targeting,
    Campaign,
    CampaignCreate,
    CampaignUpdate
)
from models.advertisers_models import (
    Advertiser,
    MLScore
)
from models.user_models import (
    Client,
)

baseurl = config.BACKEND_BASEURL

def make_campaign_put():
    targeting = Targeting(
        gender="MALE",
        age_from=10,
        age_to=20,
        location="SPB"
    )

    campaign = CampaignUpdate(
        impressions_limit=2,
        clicks_limit=2,
        cost_per_impression=randint(0, 1000),
        cost_per_click=randint(0, 500),
        ad_title="".join([choice(list("ABCDEFGH")) for _ in range(10)]),
        ad_text="".join([choice(list("ABCDEFGH")) for _ in range(10)]),
        start_date=10,
        end_date=20,
        targeting=targeting
    )

    return campaign

def make_campaign(
        age_from: int = 10, 
        age_to: int = 20,
        start_date: int = 10,
        end_date: int = 20,
        location: str = "Moscow",
        clicks_limit: int = 2,
        impressions_limit: int = 2
    ):
    targeting = Targeting(
        gender="MALE",
        age_from=age_from,
        age_to=age_to,
        location=location
    )

    campaign = CampaignCreate(
        impressions_limit=impressions_limit,
        clicks_limit=clicks_limit,
        cost_per_impression=randint(0, 1000),
        cost_per_click=randint(0, 500),
        ad_title="".join([choice(list("ABCDEFGH")) for _ in range(10)]),
        ad_text="".join([choice(list("ABCDEFGH")) for _ in range(10)]),
        start_date=start_date,
        end_date=end_date,
        targeting=targeting
    )

    return campaign

def make_campaign_on_server(
        advertiserId: str, 
        num: int,
        age_from: int = 10, 
        age_to: int = 20,
        start_date: int = 10,
        end_date: int = 20,
        location: str = "Moscow",
        clicks_limit: int = 2,
        impressions_limit: int = 2
    ) -> Tuple[List[str], List[Dict]]:
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns"

    campaigns = []
    campaign_ids = []
    for _ in range(num):
        campaign = make_campaign(age_from, age_to, start_date, end_date, location, clicks_limit, impressions_limit).model_dump()
        response = requests.post(
            url.format(advertiserId=advertiserId),
            json=campaign
        )
        campaign_ids.append(response.json().get("campaign_id"))

        campaigns.append(
            {
                "advertiser_id": advertiserId,
                "campaign_id": response.json().get("campaign_id"),
                **campaign
            }
        )

        assert response.status_code == 201
    return campaign_ids, campaigns

def get_campaign_from_server(advertiserId: str, campaignId: str) -> Tuple[Campaign, int]:
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns/{campaignId}"

    response = requests.get(
        url.format(advertiserId=advertiserId, campaignId=campaignId)
    )
    if response.status_code != 200:
        return response.json(), response.status_code

    return Campaign.model_validate(response.json()), response.status_code

def make_clients(num: int, age: Optional[int] = None, location: str = "Moscow", gender: Optional[str] = "MALE") -> List[str]:
    login = "".join([choice("ABCDEFGH") for _ in range(10)])
    location = location

    clients = [
        {
            "client_id": str(uuid4()),
            "login": login,
            "age": randint(1, 100) if not age else age,
            "location": location,
            "gender": gender
        }
        for __ in range(num)
    ]

    requests.post(
        baseurl + "/clients/bulk",
        json=clients
    )

    return [x.get("client_id") for x in clients]

def make_advertisers(num: int) -> List[str]:
    name = "".join([choice("ABCDEFGH") for _ in range(10)])

    clients = [
        {
            "advertiser_id": str(uuid4()),
            "name": name,
        }
        for __ in range(num)
    ]

    requests.post(
        baseurl + "/advertisers/bulk",
        json=clients
    )

    return [x.get("advertiser_id") for x in clients]


def make_mlscores(user_ids, advertiser_ids):
    for client in user_ids:
        for advertiser in advertiser_ids:
            response = requests.post(
                baseurl + "/ml-scores",
                json={
                    "client_id": client,
                    "advertiser_id": advertiser,
                    "score": randint(1, 100)
                }
            )
        
import requests

from core.config import config
from utils.data_service import (
    make_clients,
    make_advertisers,
    make_mlscores,
    make_campaign_on_server,
    get_campaign_from_server
)
from utils.api_service import delete_campaign

baseurl = config.BACKEND_BASEURL

def test_get_stats_full_conversion():
    # Test doesn`t work yet

    user_ids = make_clients(10, age=10, location="Belgrad")
    advertiser = make_advertisers(1)[0]

    response = requests.post(
        url=baseurl + f"/time/advance",
        json={"current_date": 20}
    )

    make_mlscores(user_ids, [advertiser]) # Создаём ML скоры
    campaign_ids, campaigns = make_campaign_on_server(
        advertiser, 1,
        age_from=10,
        age_to=20,
        start_date=10,
        end_date=20,
        location="Belgrad",
        clicks_limit=10,
        impressions_limit=10
    ) # Создаём кампании
    campaign_id = campaign_ids[0]

    for user in user_ids:
        response = requests.get(
            baseurl + "/ads",
            params={"client_id": user}
        )
        assert response.status_code == 200

        print(response.json())

        response = requests.post(
            baseurl + "/ads/{adId}/click".format(adId=campaign_id),
            json={"client_id": user}
        )
        assert response.status_code == 204

    campaign, status_code = get_campaign_from_server(advertiser, campaign_id)

    stats = {
        "impressions_count": 10,
        "clicks_count": 10,
        "conversion": 100.0,
        "spent_impressions": campaign.cost_per_impression * 10,
        "spent_clicks": campaign.cost_per_click * 10,
        "spent_total": campaign.cost_per_impression * 10 + campaign.cost_per_click * 10
    }

    # Статистика
    response = requests.get(baseurl + "/stats/campaigns/{campaignId}".format(campaignId=campaign_id)).json() # Статистика по кампании

    print(response)
    assert response == stats

    # Статистика
    response = requests.get(baseurl + "/stats/advertisers/{advertiserId}/campaigns".format(advertiserId=advertiser)).json() # Статистика по рекламодателю
    assert response == stats

    # Статистика
    response = requests.get(baseurl + "/stats/campaigns/{campaignId}/daily".format(campaignId=campaign_id)).json() # Статистика по рекламодателю
    stats["date"] = 20 
    assert stats in response

    # Статистика
    response = requests.get(baseurl + "/stats/advertisers/{advertiserId}/campaigns/daily".format(advertiserId=advertiser)).json() # Статистика по рекламодателю
    stats["date"] = 20 
    assert stats in response

    delete_campaign(campaign_id, advertiser)
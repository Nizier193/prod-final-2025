from core.config import config

from pathlib import Path
import requests

from utils.data_service import (
    make_advertisers,
    make_campaign_on_server,
    make_campaign_put,
    make_campaign
)
from utils.api_service import delete_campaign

baseurl = config.BACKEND_BASEURL
basepath = Path(config.PATH_TO_SOURCES)

def test_creating_campaign_with_anormous_title():
    """Тест создание кампании с ненормальным названием (модерация)"""
    advertisers = make_advertisers(1)[0]
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns"

    campaign = make_campaign().model_dump()
    campaign["ad_title"] = "Премьера фильма: АЛЕКСАНДР ШАХОВ Я ВАШ ФАНАТ, состоится сегодня в 10:00!"
    campaign["ad_text"] = "На сцену прибыл великий и непобедимый АЛЕКСАНДР ШАХОВ! Встречайте народного героя Александра!"

    moderated_title = 'Премьера фильма: ********* ***** * *** *****, состоится сегодня в 10:00!'
    moderated_text = 'На сцену прибыл великий и непобедимый ********* *****! Встречайте народного героя Александра!'

    # Добавляем слова в модерацию
    for bw in "АЛЕКСАНДР ШАХОВ Я ВАШ ФАНАТ".split(" "):
        response = requests.post(
            baseurl + "/moderation/banwords",
            json={"banword": bw}
        )
        assert (response.status_code in [201, 409]) # Либо создан, либо уже был создан

    # Меняем strict moderation на False
    response = requests.post(
        baseurl + "/moderation/strict",
        json={"status": False}
    )
    assert response.status_code == 200

    response = requests.post(
        url.format(advertiserId=advertisers),
        json=campaign
    )
    campaign_id = response.json().get("campaign_id")

    advertiser_id = response.json().get("advertiser_id")
    print(response.json())
    assert response.status_code == 201
    assert (response.json().get("ad_title") == moderated_title) and (response.json().get("ad_text") == moderated_text)

    # Меняем strict moderation на True
    response = requests.post(
        baseurl + "/moderation/strict",
        json={"status": True}
    )
    assert response.status_code == 200


    response = requests.post(
        url.format(advertiserId=advertisers),
        json=campaign
    )
    print(response.json())
    assert response.status_code == 400

    delete_campaign(campaign_id, advertisers)

def test_campaign_put_moderation():
    """Тест на модерацию с методом PUT"""
    advertiser = make_advertisers(1)[0]
    campaign_ids, campaigns = make_campaign_on_server(advertiser, 1)

    campaign_id, campaign = campaign_ids[0], campaigns[0]
    url = baseurl + "/advertisers/{advertiserId}" + "/campaigns/{campaignId}"

    # Меняем strict moderation на False
    response = requests.post(
        baseurl + "/moderation/strict",
        json={"status": False}
    )
    assert response.status_code == 200

    campaign_put = make_campaign_put().model_dump()
    campaign_put["ad_title"] = "Премьеры фильма АЛЕКСАНДР ШАХОВ Я ВАШ ФАНАТ не состоится!"
    campaign_put["ad_text"] = "К сожалению Александр ШАХОВ не хочет сниматься в фильме"

    moderated_title = 'Премьеры фильма ********* ***** * *** ***** не состоится!'
    moderated_text = 'К сожалению ********* ***** не хочет сниматься в фильме'

    response = requests.put(
        url.format(advertiserId=advertiser, campaignId=campaign_id),
        json=campaign_put
    )

    assert response.status_code == 200
    assert (response.json().get("ad_title") == moderated_title) and (response.json().get("ad_text") == moderated_text)

    delete_campaign(campaign_id, advertiser)

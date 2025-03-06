from core.config import config

from pathlib import Path
import requests
import time

from utils.data_service import (
    make_clients,
    make_advertisers,
    make_mlscores,
    make_campaign_on_server,
    get_campaign_from_server
)
from utils.api_service import delete_campaign

baseurl = config.BACKEND_BASEURL
basepath = Path(config.PATH_TO_SOURCES)

def test_get_ad():
    # -=-=-=-==-=-=-= 
    user_ids = make_clients(1, age=50, location="Moscow") # Юзер 15 лет
    advertiser_ids = make_advertisers(1)

    make_mlscores(user_ids, advertiser_ids) # Создаём ML скоры
    campaign_ids, campaigns = make_campaign_on_server(
        advertiser_ids[0], 
        num=1,
        age_from=45,
        age_to=55,
        start_date=10,
        end_date=20,
        location="Moscow"
    ) # Создаём кампанию полностью удовлетворяющую юзеру

    # Ставим время
    response = requests.post(
        url=baseurl + f"/time/advance",
        json={"current_date": 20}
    )
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-

    start_time = time.time()
    response = requests.get(
        baseurl + "/ads",
        params={"client_id": user_ids[0]}
    )
    assert response.status_code == 200
    assert (time.time() - start_time) < 0.2

    # Повторно, просмотр не засчитывается
    response = requests.get(
        baseurl + "/ads",
        params={"client_id": user_ids[0]}
    )
    assert response.status_code == 404

    delete_campaign(campaign_ids[0], advertiser_ids[0])



def test_get_no_ad():
    # -=-=-=-==-=-=-= подготовка
    user_ids = make_clients(1, age=65, location="Moscow") # Юзер 65 лет
    advertiser_ids = make_advertisers(1)

    make_mlscores(user_ids, advertiser_ids) # Создаём ML скоры
    campaign_ids, campaigns = make_campaign_on_server(
        advertiser_ids[0], 
        num=1,
        age_from=45,
        age_to=55,
        start_date=10,
        end_date=20,
        location="Moscow"
    ) # Кампания не удовлетворяет юзеру

    start_time = time.time()
    response = requests.get(
        baseurl + "/ads",
        params={"client_id": user_ids[0]}
    )
    assert response.status_code == 404
    assert (time.time() - start_time) < 0.2

    delete_campaign(campaign_ids[0], advertiser_ids[0])



def test_get_ad_wrong_time():
    # -=-=-=-==-=-=-= подготовка
    user_ids = make_clients(1, age=50, location="Moscow") # Юзер 15 лет
    advertiser_ids = make_advertisers(1)

    make_mlscores(user_ids, advertiser_ids) # Создаём ML скоры
    campaign_ids, campaigns = make_campaign_on_server(
        advertiser_ids[0], 
        num=1,
        age_from=45,
        age_to=55,
        start_date=10,
        end_date=20,
        location="Moscow"
    ) # Создаём кампанию полностью удовлетворяющую юзеру

    # Ставим время, не подходит под кампанию
    response = requests.post(
        url=baseurl + f"/time/advance",
        json={"current_date": 60}
    )
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-

    start_time = time.time()
    response = requests.get(
        baseurl + "/ads",
        params={"client_id": user_ids[0]}
    )
    assert response.status_code == 404
    assert (time.time() - start_time) < 0.2

    delete_campaign(campaign_ids[0], advertiser_ids[0])



def test_get_ad_wrong_location():
    # -=-=-=-==-=-=-= подготовка
    user_ids = make_clients(1, age=50, location="MOSCOW") # Юзер 15 лет
    advertiser_ids = make_advertisers(1)

    make_mlscores(user_ids, advertiser_ids) # Создаём ML скоры
    campaign_ids, campaigns = make_campaign_on_server(
        advertiser_ids[0], 
        num=1,
        age_from=45,
        age_to=55,
        start_date=10,
        end_date=20,
        location="Moscow"
    ) # Кампания не подходит из-за того, что локация не полностью совпадает

    # Ставим время, не подходит под кампанию
    response = requests.post(
        url=baseurl + f"/time/advance",
        json={"current_date": 20}
    )
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-

    start_time = time.time()
    response = requests.get(
        baseurl + "/ads",
        params={"client_id": user_ids[0]}
    )
    assert response.status_code == 404
    assert (time.time() - start_time) < 0.2

    delete_campaign(campaign_ids[0], advertiser_ids[0])



def test_click_ad():
    user_ids = make_clients(1)
    advertiser_ids = make_advertisers(1)

    make_mlscores(user_ids, advertiser_ids) # Создаём ML скоры
    campaign_ids, campaigns = make_campaign_on_server(advertiser_ids[0], 1) # Создаём кампании

    response = requests.post(
        baseurl + "/ads/{adId}/click".format(adId=campaign_ids[0]),
        json={"client_id": user_ids[0]}
    )
    print(response.content)
    assert response.status_code == 204

    # Повторно клик не засчитывается
    response = requests.post(
        baseurl + "/ads/{adId}/click".format(adId=campaign_ids[0]),
        json={"client_id": user_ids[0]}
    )
    assert response.status_code == 200

    delete_campaign(campaign_ids[0], advertiser_ids[0])

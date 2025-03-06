from core.config import config

from uuid import uuid4
from pathlib import Path
import requests

from utils.data_service import (
    make_advertisers,
    make_campaign_on_server
)
from utils.api_service import delete_campaign

baseurl = config.BACKEND_BASEURL
basepath = Path(config.PATH_TO_SOURCES) / Path("images")

path_to_download = basepath / Path("images_from_server")
path_to_download.mkdir(exist_ok=True)

def test_campaign_put_image():
    advertiser = make_advertisers(1)[0]
    campaign_ids, campaigns = make_campaign_on_server(advertiser, 1)

    campaign_id, campaign = campaign_ids[0], campaigns[0]
    url = baseurl + "/images/{campaignId}"

    response = requests.post(
        url=url.format(campaignId=campaign_id),
        files={
            "image": open(basepath / Path("image.jpg"), "rb")
        }
    )
    response = requests.post(
        url=url.format(campaignId=campaign_id),
        files={
            "image": open(basepath / Path("image2.jpg"), "rb")
        }
    )
    response = requests.post(
        url=url.format(campaignId=campaign_id),
        files={
            "image": open(basepath / Path("image3.jpg"), "rb")
        }
    )
    response = requests.post(
        url=url.format(campaignId=campaign_id),
        files={
            "image": open(basepath / Path("image.jpg"), "rb")
        }
    )

    key = response.json().get("key")
    assert response.status_code == 201

    response = requests.get(
        url=url.format(campaignId=campaign_id),
    )


    response = requests.get(baseurl + "/images", params={"key": key})
    assert response.status_code == 200

    # Открываем файл для записи в бинарном режиме
    with open(path_to_download / Path(f"image-{str(uuid4())[:15]}.jpg"), "wb") as file:
        file.write(response.content)


    # response.json() : List[Dict[key, url, status]]
    response = requests.get(baseurl + f"/images/{campaign_id}")
    assert len(response.json()) == 4

    delete_campaign(campaign_id, advertiser)
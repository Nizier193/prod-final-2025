from core.config import config

import requests
from pathlib import Path
import json

baseurl = config.BACKEND_BASEURL
basepath = Path(config.PATH_TO_SOURCES) / Path("advertiser_json")

def test_creating_advertisers_ok():
    """Создание нормальных рекламодателей -> 200"""
    url = baseurl + "/advertisers/bulk"

    advertisers_json = json.load(open(basepath / Path("advertisers_ok.json"), "r"))

    response = requests.post(
        url,
        json=advertisers_json
    )

    assert response.status_code == 201
    assert response.json() == advertisers_json


def test_creating_advertisers_broken():
    """Создание ненормальных рекламодателей -> 400"""
    url = baseurl + "/advertisers/bulk"

    advertisers_json = json.load(open(basepath / Path("advertisers_broken.json"), "r"))

    for broken in advertisers_json:
        response = requests.post(
            url,
            json=[broken]
        )

        assert response.status_code == 400

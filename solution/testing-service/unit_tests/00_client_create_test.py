from core.config import config

from pathlib import Path
import requests
import json

baseurl = config.BACKEND_BASEURL
basepath = Path(config.PATH_TO_SOURCES) / Path("user_json")

def test_creating_normal_users():
    """Создание нормальных пользователей -> 200"""
    user_creating_url = baseurl + "/clients/bulk"

    json_path = basepath / Path("users_ok.json")
    client_jsons = json.load(open(json_path, "r"))

    response = requests.post(
        user_creating_url,
        json=client_jsons
    )

    assert response.status_code == 201
    assert response.json() == client_jsons


def test_creating_broken_users():
    """Создание не нормальных пользователей -> 400"""
    user_creating_url = baseurl + "/clients/bulk"

    json_path = basepath / Path("users_broken.json")
    client_jsons = json.load(open(json_path, "r"))

    for broken in client_jsons:
        response = requests.post(
            user_creating_url,
            json=[broken]
        )

        assert response.status_code == 400

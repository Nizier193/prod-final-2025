from core.config import config

from random import randint
from uuid import uuid4
import requests

from utils.data_service import (
    make_clients,
    make_advertisers
)

baseurl = config.BACKEND_BASEURL

def test_normal_mlscores():
    """Создание обычных ML Скоров"""
    clients = make_clients(10)
    advertisers = make_advertisers(10)

    for client in clients:
        for advertiser in advertisers:
            response = requests.post(
                baseurl + "/ml-scores",
                json={
                    "client_id": client,
                    "advertiser_id": advertiser,
                    "score": randint(1, 100)
                }
            )
            assert response.status_code == 200


def test_clients_not_exist():
    """Клиента не существует с которым связан ML Скор"""
    clients = [str(uuid4()) for _ in range(10)] # Несуществующие
    advertisers = make_advertisers(10)

    for client in clients:
        for advertiser in advertisers:
            response = requests.post(
                baseurl + "/ml-scores",
                json={
                    "client_id": client,
                    "advertiser_id": advertiser,
                    "score": randint(1, 100)
                }
            )
            assert response.status_code == 404


def test_advertisers_not_exist():
    """Рекламодателя не существует с которым связан ML Скор"""
    clients = make_clients(10) # Несуществующие
    advertisers = [str(uuid4()) for _ in range(10)]

    for client in clients:
        for advertiser in advertisers:
            response = requests.post(
                baseurl + "/ml-scores",
                json={
                    "client_id": client,
                    "advertiser_id": advertiser,
                    "score": randint(1, 100)
                }
            )
            assert response.status_code == 404


def test_mlscore_not_integer():
    """ML Скор - не число"""
    clients = make_clients(10)
    advertisers = make_advertisers(10)

    for client in clients:
        for advertiser in advertisers:
            response = requests.post(
                baseurl + "/ml-scores",
                json={
                    "client_id": client,
                    "advertiser_id": advertiser,
                    "score": "123"
                }
            )
            assert response.status_code == 400
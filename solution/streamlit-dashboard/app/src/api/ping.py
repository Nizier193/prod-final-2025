import requests
from core.config import config

def get_ping():
    response = requests.get(
        config.BACKEND_BASEURL.rstrip("/") + "/ping"
    )
    return response.status_code
import requests

from core.config import config

baseurl = config.BACKEND_BASEURL

def test_set_time():
    response = requests.post(
        url=baseurl + f"/time/advance",
        json={"current_date": 20}
    )
    assert response.status_code == 200
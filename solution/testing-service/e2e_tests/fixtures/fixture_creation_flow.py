from uuid import uuid4
import pytest

@pytest.fixture
def creationFlowData():
    advertiserId = str(uuid4())

    class TestData:
        banword = "школа"
        advertiser_id = advertiserId
        advertiser = [{"advertiser_id": advertiserId, "name": "some advertiser name"}]
        campaign = {
            "impressions_limit": 1000,
            "clicks_limit": 100,
            "cost_per_impression": 0.5,
            "cost_per_click": 2.0,
            "ad_title": "Школа №416 отчаянно нуждается в кадрах!",
            "ad_text": "ГБОУ Средняя Общеобразовательная Школа ищет сотрудников.",
            "start_date": 1,
            "end_date": 50,
            "targeting": {
                "gender": "MALE",
                "age_from": 25,
                "age_to": 45,
                "location": "New York"
            }
        }
        censored_ad_text = "ГБОУ Средняя Общеобразовательная ***** ищет сотрудников."
        campaign_put_normal = {
            "impressions_limit": 1000,
            "clicks_limit": 100,
            "cost_per_impression": 0.5,
            "cost_per_click": 2.0,
            "ad_title": "№416 отчаянно нуждается в кадрах!",
            "ad_text": "ГБОУ Средняя Общеобразовательная ищет сотрудников.",
            "start_date": 1,
            "end_date": 50,
            "targeting": {
                "gender": "MALE",
                "age_from": 25,
                "age_to": 45,
                "location": "New York"
            }
        }
        
    return TestData
from e2e_tests.helpers.backend_client import BackendAPIService
from e2e_tests.fixtures.fixture_creation_flow import creationFlowData

service = BackendAPIService()

"""Тест на успешное создание кампаний, управление их контентом и модерация"""
def test_full_create_flow(creationFlowData):

    # Создание рекламодателей
    advertisers, status = service.create_advertisers_bulk(
        advertisers=creationFlowData.advertiser, 
        expected_status=201
    )
    assert status

    # Добавление в модерацию банворда
    banwords, status = service.moderation_add_banwords(
        banword=creationFlowData.banword, 
        expected_status=201
    )
    assert status or (banwords.status_code == 409) # Если слово уже есть в банвордах

    # Включение нестрогой модерации
    moderation, status = service.moderation_strict(
        status=False, 
        expected_status=200
    )
    assert status

    # Создание кампании
    campaign, status = service.create_campaign(
        advertiserId=creationFlowData.advertiser_id, 
        campaign=creationFlowData.campaign, 
        expected_status=201
    )
    assert status

    # Проверка на модерацию
    campaign_json = campaign.json()
    assert campaign_json.get("ad_text") == creationFlowData.censored_ad_text

    # Включение строгой модерации
    moderation, status = service.moderation_strict(
        status=True, 
        expected_status=200
    )
    assert status

    # Изменение на неправильный контент
    changed_campaign, status = service.put_campaign(
        advertiserId=creationFlowData.advertiser_id,
        campaignId=campaign_json.get("campaign_id"),
        campaignPut=creationFlowData.campaign,
        expected_status=400
    )
    assert status

    # Изменение на правильный контент
    changed_campaign, status = service.put_campaign(
        advertiserId=creationFlowData.advertiser_id,
        campaignId=campaign_json.get("campaign_id"),
        campaignPut=creationFlowData.campaign_put_normal,
        expected_status=200
    )
    assert status

    # Удаление кампании
    deleted_campaign, status = service.delete_campaign(
        advertiserId=creationFlowData.advertiser_id,
        campaignId=campaign_json.get("campaign_id"),
        expected_status=204
    )
    assert status



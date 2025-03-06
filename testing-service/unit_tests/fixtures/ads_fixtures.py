import pytest

def get_empty_target_campaign():
    campaign = {
        'impressions_limit': 10, 
        'clicks_limit': 10, 
        'cost_per_impression': 1.0, 
        'cost_per_click': 1.0, 
        'ad_title': '123', 
        'ad_text': '123', 
        'start_date': 10, 
        'end_date': 20, 
        'targeting': {
            'gender': None, 
            'age_from': None, 
            'age_to': None, 
            'location': None
        }
    }
    return campaign

@pytest.fixture()
def campaigns_empty_target():
    return [get_empty_target_campaign()] * 5


@pytest.fixture()
def campaign_gender_target():
    """Gender """
    gender_target_campaign_M = get_empty_target_campaign()
    gender_target_campaign_M["targeting"]["gender"] = "MALE"

    gender_target_campaign_F = get_empty_target_campaign()
    gender_target_campaign_F["targeting"]["gender"] = "FEMALE"

    return [gender_target_campaign_M] * 5, [gender_target_campaign_F] * 5


@pytest.fixture()
def campaign_location_target():
    """Target"""
    target_campaign_kazan = get_empty_target_campaign()
    target_campaign_kazan["targeting"]["location"] = "kazan"

    target_campaign_msk = get_empty_target_campaign()
    target_campaign_msk["targeting"]["location"] = "msk"

    target_campaign_spb = get_empty_target_campaign()
    target_campaign_spb["targeting"]["location"] = "spb"

    target_campaign_taiga = get_empty_target_campaign()
    target_campaign_taiga["targeting"]["location"] = "taiga"

    return [
        target_campaign_kazan,
        target_campaign_msk,
        target_campaign_spb,
        target_campaign_taiga
    ]


@pytest.fixture()
def campaigns_age_target():
    low_age = get_empty_target_campaign()
    low_age["targeting"]["age_from"] = 2
    low_age["targeting"]["age_to"] = 10

    medium_age = get_empty_target_campaign()
    medium_age["targeting"]["age_from"] = 10
    medium_age["targeting"]["age_to"] = 20

    high_age = get_empty_target_campaign()
    high_age["targeting"]["age_from"] = 70
    high_age["targeting"]["age_to"] = 80

    return [
        low_age,
        medium_age,
        high_age
    ]
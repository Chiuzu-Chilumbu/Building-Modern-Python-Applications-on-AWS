"""in this module we write unit test for out dragon API using pytest"""

import pytest
from  api.dragons_api import DragonsAPI

@pytest.fixture(scope='function')
def dragons():
    return DragonsAPI()


def test_dragon_name(dragons_api):
    response = dragons_api.dragon_name("Herma")
    assert "TestDragon" in response

def test_dragon_family(dragons_api):
    response = dragons_api.dragon_family("black")
    assert response

def test_dragon_list(dragons_api):
    response = dragons_api.dragon_list()
    assert response 

def test_create_dragon(dragons_api):
    dragon_attributes = {
        "description_str": "A fierce fire-breathing dragon.",
        "dragon_name_str": "Draco",
        "family_str": "Fire",
        "location_city_str": "Mordor",
        "location_country_str": "MiddleEarth",
        "location_neighborhood_str": "Mount Doom",
        "location_state_str": "Gorgoroth"
    }
    response = dragons_api.create_dragon(dragon_attributes)
    # Assert that the response indicates success, replace 201 with your API's success status code
    assert response.status_code == 200
    # Clean up any resources created if necessary

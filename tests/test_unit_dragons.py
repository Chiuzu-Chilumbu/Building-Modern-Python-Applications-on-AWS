"""in this module we write unit test for out dragon API using pytest"""

from unittest.mock import patch
from api.dragons_api import DragonsAPI
import pytest
import  json


# Assuming your fixture is named 'dragons', not 'dragons_api'
@pytest.fixture(scope='module')
def dragons():
    # Initialize the DragonsAPI class instance
    return DragonsAPI()

def test_can_create_dragon_api_class(dragons):
    # Act, Arrange & Assert
    assert isinstance(dragons, DragonsAPI)


def test_dragon_api_class_contains_aws_invoke_url(dragons):
    # Act & Arrange, Assert
    assert dragons.DRAGONS_API_ENDPOINT == "https://tqibofk44h.execute-api.ap-northeast-3.amazonaws.com/testing/dragons"



# Mocking the requests.request call to test the dragon_name function 
@patch('api.dragons_api.requests.request')
def test_dragon_data_can_be_obtained_by_name(mock_get, dragons):

    # Arrange
    expected_response = {
      "description_str": "Herma is a wise water sage dragon. Dragons travel from all the land to seek her counsel and her wisdom.",
      "dragon_name_str": "Herma",
      "family_str": "blue",
      "location_city_str": "twin falls",
      "location_country_str": "usa",
      "location_neighborhood_str": "applewood dr",
      "location_state_str": "idaho"
   }
    
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = expected_response
    mock_get.return_value.text = json.dumps(expected_response)

    # Act
    response = dragons.dragon_name("TestDragon")

    # Assert
    mock_get.assert_called_once_with(
        "GET",
        f"{dragons.DRAGONS_API_ENDPOINT}?dragonName=TestDragon",
        headers={'Authorization': dragons.authorisation_token, 'Content-Type': 'application/json'},
        data={},
        timeout=5
    )

    # Since the dragon_name method returns response.text, we assert that the response
    # is the string representation of the expected_response
    assert response == json.dumps(expected_response)

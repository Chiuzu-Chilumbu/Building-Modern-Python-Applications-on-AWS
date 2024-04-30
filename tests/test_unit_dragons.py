"""in this module we write unit test for out dragon API using pytest"""

import pytest
from unittest.mock import patch
from api.dragons_api import DragonsAPI

@pytest.fixture(scope='function')
def dragons():
    return DragonsAPI()


def test_can_create_dragon_api_class(dragons):
    # Act, Arrange & Assert
    assert isinstance(dragons, DragonsAPI)


def test_dragon_api_class_contains_aws_invoke_url(dragons):
    # Act & Arrange, Assert
    assert dragons.DRAGONS_API_ENDPOINT == "https://tqibofk44h.execute-api.ap-northeast-3.amazonaws.com/testing/dragons"


# mocking the request call to test the dragon_name function 
@patch('dragons_api.reqeusts.request')
def test_dragon_data_can_be_obtained_by_name(mock_get, DragonsAPI):
    # Arrange
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'name': 'TestDragon', 'family': 'TestFamily'}


    # Act 
    response = DragonsAPI.dragon_name("TestDragon")

    # Assert 
    mock_get.assert_called_once_with(
        "GET",
        f"{DragonsAPI.DRAGONS_API_ENDPOINT}?dragonName=TestDragon",
        headers={'Authorization': DragonsAPI.authorisation_token, 'Content-Type': 'application/json'},
        data={},
        timeout=5
    )
    assert response == {'name': 'TestDragon', 'family': 'TestFamily'}

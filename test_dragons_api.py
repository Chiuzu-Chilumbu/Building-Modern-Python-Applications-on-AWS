"""in this module we write unit test for out dragon API using pytest"""

import pytest
from dragons_api import DragonsAPI

@pytest.fixture(scope='function')
def dragons():
    return DragonsAPI()


def test_can_create_dragon_api_class(dragons):
    # Act, Arrange & Assert
    assert isinstance(dragons, DragonsAPI)


def test_dragon_api_class_contains_aws_invoke_url(dragons):
    # Act & Arrange, Assert
    assert dragons.DRAGONS_API_ENDPOINT == "https://tqibofk44h.execute-api.ap-northeast-3.amazonaws.com/testing/dragons"


def test_dragon_data_can_be_obtained_by_name(dragons):
    pass

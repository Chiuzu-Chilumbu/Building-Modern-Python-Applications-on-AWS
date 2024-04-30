"""in this module we write unit test for out dragon API using pytest"""

import pytest
from  api.dragons_api import DragonsAPI

@pytest.fixture(scope='function')
def dragons():
    return DragonsAPI()


def test_dragon_name(dragons):
    response = dragons.dragon_name("Herma")
    assert "Herma" in response 

def test_dragon_family(dragons):
    response = dragons.dragon_family("black")
    assert "black" in response


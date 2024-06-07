"""in this module we test the add dragon lambda handler"""

from unittest.mock import patch
import boto3
import pytest
from botocore.stub import Stubber
import json
from AddDragon.addDragon import addDragonToFile

@pytest.fixture
def ssm_stub():
    with Stubber(boto3.client('ssm', region_name='ap-northeast-3')) as stubber:
        stubber.add_response('get_parameter', {
            'Parameter': {'Value': 'test-bucket'}
        }, {'Name': 'dragon_data_bucket_name', 'WithDecryption': False})
        stubber.add_response('get_parameter', {
            'Parameter': {'Value': 'test-file.json'}
        }, {'Name': 'dragon_data_file_name', 'WithDecryption': False})
        yield stubber
        stubber.deactivate()

@pytest.fixture
def s3_stub():
    with Stubber(boto3.client('s3', region_name='ap-northeast-3')) as stubber:
        get_object_response = {
            'Body': b'[{"description_str":"Existing dragon","dragon_name_str":"Existing","family_str":"red","location_city_str":"City","location_country_str":"Country","location_neighborhood_str":"Neighborhood","location_state_str":"State"}]'
        }
        stubber.add_response('get_object', get_object_response, {
            'Bucket': 'test-bucket',
            'Key': 'test-file.json'
        })

        put_object_response = {}
        stubber.add_response('put_object', put_object_response, {
            'Bucket': 'test-bucket',
            'Key': 'test-file.json',
            'Body': json.dumps([{
                "description_str": "Some say Inexistente doesn't exist, yet.",
                "dragon_name_str": "Inexistente",
                "family_str": "green",
                "location_city_str": "seattle",
                "location_country_str": "usa",
                "location_neighborhood_str": "4th st",
                "location_state_str": "washington"
            }, {
                "description_str":"Existing dragon",
                "dragon_name_str":"Existing",
                "family_str":"red",
                "location_city_str":"City",
                "location_country_str":"Country",
                "location_neighborhood_str":"Neighborhood",
                "location_state_str":"State"
            }])
        })
        yield stubber
        stubber.deactivate()

@patch('boto3.client')
def test_add_dragon(mock_boto_client, ssm_stub, s3_stub):
    mock_boto_client.side_effect = [ssm_stub.client, s3_stub.client]
    event = {
        "description_str": "Some say Inexistente doesn't exist, yet.",
        "dragon_name_str": "Inexistente",
        "family_str": "green",
        "location_city_str": "seattle",
        "location_country_str": "usa",
        "location_neighborhood_str": "4th st",
        "location_state_str": "washington"
    }
    context = {}

    result = addDragonToFile(event, context)
    
    assert isinstance(result, dict)
    assert result['statusCode'] == 200
    assert result['body'] is None

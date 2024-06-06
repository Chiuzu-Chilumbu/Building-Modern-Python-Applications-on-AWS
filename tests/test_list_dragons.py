"""In this module we test the lambda function list dragon"""

from unittest.mock import patch
import boto3
import pytest
from botocore.stub import Stubber
import json
from ListDragons.listDragons import listDragons  # Replace 'your_module' with the actual module name

@pytest.fixture
def mock_ssm_client():
    with Stubber(boto3.client('ssm', region_name='ap-northeast-3')) as stubber:
        stubber.add_response('get_parameter', {
            'Parameter': {'Value': 'your-bucket-name'}
        }, {'Name': 'dragon_data_bucket_name', 'WithDecryption': False})
        stubber.add_response('get_parameter', {
            'Parameter': {'Value': 'your-file-name.json'}
        }, {'Name': 'dragon_data_file_name', 'WithDecryption': False})
        yield stubber
        stubber.deactivate()

@pytest.fixture
def mock_s3_client():
    with Stubber(boto3.client('s3', region_name='ap-northeast-3')) as stubber:
        payload = {
            'Payload': [
                {
                    'Records': {
                        'Payload': b'{"dragon_name_str": "Atlas", "family_str": "red"}\n'
                    }
                }
            ]
        }
        stubber.add_response('select_object_content', payload, {
            'Bucket': 'your-bucket-name',
            'Key': 'your-file-name.json',
            'ExpressionType': 'SQL',
            'Expression': "select * from s3object[*][*] s",
            'InputSerialization': {'JSON': {'Type': 'Document'}},
            'OutputSerialization': {'JSON': {}}
        })
        yield stubber
        stubber.deactivate()

@patch('boto3.client')
def test_list_dragons_json_response(mock_boto_client, mock_ssm_client, mock_s3_client):
    mock_boto_client.side_effect = lambda service, region_name: {
        'ssm': mock_ssm_client.client,
        's3': mock_s3_client.client,
    }[service]
    
    event = {
        'queryStringParameters': {
            'dragonName': 'Atlas'
        }
    }
    context = {}
    result = listDragons(event, context)
    assert isinstance(result, dict)
    assert result['statusCode'] == 200
    body = result['body']
    body_json = json.loads(body)
    assert 'dragon_name_str' in body_json
    assert 'family_str' in body_json

@patch('boto3.client')
def test_list_dragons_contains_expected_attributes(mock_boto_client, mock_ssm_client, mock_s3_client):
    mock_boto_client.side_effect = lambda service, region_name: {
        'ssm': mock_ssm_client.client,
        's3': mock_s3_client.client,
    }[service]
    
    event = {
        'queryStringParameters': {
            'dragonName': 'Atlas'
        }
    }
    context = {}
    result = listDragons(event, context)
    body = result['body']
    body_json = json.loads(body)
    assert 'dragon_name_str' in body_json
    assert 'family_str' in body_json
    assert body_json['dragon_name_str'] == 'Atlas'
    assert body_json['family_str'] == 'red'

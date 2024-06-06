from unittest.mock import patch
import boto3
import pytest
from botocore.stub import Stubber
import json
from ListDragons.listDragons import listDragons  # Replace 'your_module' with the actual module name

@pytest.fixture
def ssm_stub():
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
def s3_stub():
    with Stubber(boto3.client('s3', region_name='ap-northeast-3')) as stubber:
        payload = {
            'Payload': {
                'Records': {
                    'Payload': b'{"dragon_name_str": "Atlas", "family_str": "red"}\n'
                }
            }
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
def test_list_dragons_json_response(mock_boto_client, ssm_stub, s3_stub):
    mock_boto_client.side_effect = [ssm_stub.client, s3_stub.client]
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
    # Convert body_json to a list if it's not
    if isinstance(body_json, str):
        body_json = json.loads(body_json)
    assert 'dragon_name_str' in body_json
    assert 'family_str' in body_json

@patch('boto3.client')
def test_list_dragons_contains_expected_attributes(mock_boto_client, ssm_stub, s3_stub):
    mock_boto_client.side_effect = [ssm_stub.client, s3_stub.client]
    event = {
        'queryStringParameters': {
            'dragonName': 'Atlas'
        }
    }
    context = {}
    result = listDragons(event, context)
    body = result['body']
    body_json = json.loads(body)
    # Convert body_json to a list if it's not
    if isinstance(body_json, str):
        body_json = json.loads(body_json)
    assert 'dragon_name_str' in body_json
    assert 'family_str' in body_json
    assert body_json['dragon_name_str'] == 'Atlas'
    assert body_json['family_str'] == 'red'

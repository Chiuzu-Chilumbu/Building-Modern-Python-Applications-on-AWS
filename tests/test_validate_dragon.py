"""in this module we test the validate dragon lambda handler"""

from unittest.mock import patch
import boto3
import pytest
from botocore.stub import Stubber
from lambda_handlers.ValidateDragon.validateDragon import validate, DragonValidationException

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
def s3_stub_existing_dragon():
    with Stubber(boto3.client('s3', region_name='ap-northeast-3')) as stubber:
        payload = {
            'Payload': {
                'Records': {
                    'Payload': b'{"dragon_name_str": "Shadow", "family_str": "black"}\n'
                }
            }
        }
        stubber.add_response('select_object_content', payload, {
            'Bucket': 'test-bucket',
            'Key': 'test-file.json',
            'ExpressionType': 'SQL',
            'Expression': "select * from S3Object[*][*] s where s.dragon_name_str = 'Shadow'",
            'InputSerialization': {'JSON': {'Type': 'Document'}},
            'OutputSerialization': {'JSON': {}}
        })
        yield stubber
        stubber.deactivate()

@pytest.fixture
def s3_stub_new_dragon():
    with Stubber(boto3.client('s3', region_name='ap-northeast-3')) as stubber:
        payload = {
            'Payload': {}
        }
        stubber.add_response('select_object_content', payload, {
            'Bucket': 'test-bucket',
            'Key': 'test-file.json',
            'ExpressionType': 'SQL',
            'Expression': "select * from S3Object[*][*] s where s.dragon_name_str = 'Inexistente'",
            'InputSerialization': {'JSON': {'Type': 'Document'}},
            'OutputSerialization': {'JSON': {}}
        })
        yield stubber
        stubber.deactivate()

@patch('boto3.client')
def test_validate_existing_dragon(mock_boto_client, ssm_stub, s3_stub_existing_dragon):
    mock_boto_client.side_effect = [ssm_stub.client, s3_stub_existing_dragon.client]
    event = {
        'dragon_name_str': 'Shadow'
    }
    context = {}
    with pytest.raises(DragonValidationException) as excinfo:
        validate(event, context)
    assert str(excinfo.value) == "DragonValidationException, Duplicate dragon reported"


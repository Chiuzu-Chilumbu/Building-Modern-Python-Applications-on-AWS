"""Add Dragon Lambda function handler driver code"""

import boto3
import json

# Declare variables outside handler to reduce initialization on startup
s3 = boto3.client('s3', 'ap-northeast-3')
ssm = boto3.client('ssm', 'ap-northeast-3')
bucket_name = ssm.get_parameter(
    Name='dragon_data_bucket_name',
    WithDecryption=False)['Parameter']['Value']
file_name = ssm.get_parameter(
    Name='dragon_data_file_name',
    WithDecryption=False)['Parameter']['Value']


def addDragonToFile(event, context):
    dragon_data = {
        "description_str": event['description_str'],
        "dragon_name_str": event['dragon_name_str'],
        "family_str": event['family_str'],
        "location_city_str": event['location_city_str'],
        "location_country_str": event['location_country_str'],
        "location_neighborhood_str": event['location_neighborhood_str'],
        "location_state_str": event['location_state_str']
    }

    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    data = response.get('Body').read()

    json_data = json.loads(data)
    json_data.append(dragon_data)
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json.dumps(json_data).encode())

    return {
        "statusCode": 200,
        "body": None
    }

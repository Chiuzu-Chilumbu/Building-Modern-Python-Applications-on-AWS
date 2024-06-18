"""In this module we create the add dragon lambda handler"""

import boto3
import json

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

    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        data = response.get('Body').read()
        json_data = json.loads(data)
    except Exception as e:
        raise Exception(f"Error retrieving or parsing S3 object: {str(e)}")

    json_data.append(dragon_data)

    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(json_data).encode())
    except Exception as e:
        raise Exception(f"Error uploading updated data to S3: {str(e)}")
    
    return {
        "statusCode": 200,
        "body": None
    }
    
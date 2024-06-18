"""List Dragons Lambda function handler driver code"""

import boto3
import json

# Declare variables outside handler to reduce initialization on startup
s3 = boto3.client('s3', 'ap-northeast-3')
ssm = boto3.client('ssm', 'ap-northeast-3')
bucket_name = ssm.get_parameter(Name='dragon_data_bucket_name', WithDecryption=False)['Parameter']['Value']
file_name = ssm.get_parameter(Name='dragon_data_file_name', WithDecryption=False)['Parameter']['Value']

def listDragons(event, context):
    """
    List dragons stored in S3 bucket
    """
    expression = "select * from s3object[*][*] s"
    
    if 'queryStringParameters' in event and event['queryStringParameters'] is not None:
        if 'dragonName' in event['queryStringParameters']:
            expression = f"select * from S3Object[*][*] s where s.dragon_name_str = '{event['queryStringParameters']['dragonName']}'"
        if 'family' in event['queryStringParameters']:
            expression = f"select * from S3Object[*][*] s where s.family_str = '{event['queryStringParameters']['family']}'"
    
    try:
        result = s3.select_object_content(
            Bucket=bucket_name,
            Key=file_name,
            ExpressionType='SQL',
            Expression=expression,
            InputSerialization={'JSON': {'Type': 'Document'}},
            OutputSerialization={'JSON': {}}
        )
    
        records = ''
        for event in result['Payload']:
            if 'Records' in event:
                records += event['Records']['Payload'].decode('utf-8')
    
        return {
            "statusCode": 200,
            "body": json.dumps(records)
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

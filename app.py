"""this module is the driver code for the dragons API"""

import boto3

s3 = boto3.resource('s3', 'ap-northeast-3').meta.client
ssm = boto3.client('ssm', 'ap-northeast-3')


def list_dragons(bucket_name, file_name):
    """this method uses a SQL like query to obtain the full dragons list"""
    expression = "select * from s3object s"

    result = s3.select_object_content(
        Bucket=bucket_name,
        Key=file_name,
        ExpressionType='SQL',
        Expression=expression,
        InputSerialization={'JSON': {'Type': 'Document'}},
        OutputSerialization={'JSON': {}}
    )

    for event in result['Payload']:
        if 'Records' in event:
            print(event['Records']['Payload'].decode('utf-8'))


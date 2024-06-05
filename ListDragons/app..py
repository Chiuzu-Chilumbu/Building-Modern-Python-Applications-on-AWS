"""Leverage SSM to obtain bucket information"""

import boto3

# Initialize the S3 and SSM clients
s3 = boto3.client('s3', 'ap-northeast-3')
ssm = boto3.client('ssm', 'ap-northeast-3')

# Retrieve the parameters from SSM
bucket_name = ssm.get_parameter(Name='dragon_data_bucket_name', WithDecryption=False)['Parameter']['Value']
file_name = ssm.get_parameter(Name='dragon_data_file_name', WithDecryption=False)['Parameter']['Value']

def listDragons():
    """List dragons stored in S3 bucket"""
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



if __name__ == '__main__':
    listDragons()

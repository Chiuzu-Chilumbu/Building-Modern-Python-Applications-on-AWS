"""In this module we create a validate dragons lambda function handler"""

import boto3

s3 = boto3.client('s3', 'ap-northeast-3')
ssm = boto3.client('ssm', 'ap-northeast-3')

bucket_name = ssm.get_parameter(Name='dragon_data_bucket_name', WithDecryption=False)['Parameter']['Value']
file_name = ssm.get_parameter(Name='dragon_data_file_name', WithDecryption=False)['Parameter']['Value']

def validate(event, context):
    """Validate dragon handler"""
    result = s3.select_object_content(
        Bucket=bucket_name,
        Key=file_name,
        ExpressionType='SQL',
        Expression="select * from S3Object[*][*] s where s.dragon_name_str = '" + event['dragon_name_str'] + "'",
        InputSerialization={'JSON': {'Type': 'Document'}},
        OutputSerialization={'JSON': {}}
    )

    for records in result['Payload']:
        if 'Records' in records:
            raise DragonValidationException("Duplicate dragon reported")

    return 'Dragon Validated'

class DragonValidationException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"DragonValidationException, {self.message}"
        else:
            return f"DragonValidationException has been raised"


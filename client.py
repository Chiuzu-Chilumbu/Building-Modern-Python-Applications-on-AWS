"""
This module demonstrates how to use boto3 to acces and AWS services through:
client : low-level service access
"""
import boto3


def access_s3_bucket(bucket_name):
    """this function provides access to an s3 bucket based on its name"""
    client = boto3.client('s3')
    response = client.list_objects(Bucket=bucket_name)

    # show bucket content
    for content in response['Contents']:
        obj_dict = client.get_object(Bucket=bucket_name, key=content['Key'])
        print(content['key'], obj_dict['lastModified'])



access_s3_bucket('exerciseone')
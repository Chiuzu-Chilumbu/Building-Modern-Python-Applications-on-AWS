"""
This module demonstrates how to use boto3 to acces and AWS services through:
client : low-level service access
"""
import json
import boto3

def access_s3_bucket(bucket_name):
    """This function provides access to an s3 bucket based on its name"""
    # create an S3 client
    client = boto3.client('s3')

    # retrieve the object (file) from the bucket
    response = client.list_objects(Bucket=bucket_name)

    # show bucket content
    for content in response['Contents']:
        obj_dict = client.get_object(Bucket=bucket_name, key=content['Key'])
        print(content['key'], obj_dict['lastModified'])



def access_s3_bucket_file_data(bucket_name, file_name):
    """This function prints the content of the JSON file stored in the S3 bucket"""

    # create an S3 client
    client = boto3.client('s3')

    # retrieve the object (file) from the bucket
    obj = client.get_object(Bucket=bucket_name, Key=file_name)

    # object['body'] is the file object. we read it into a string
    json_string = obj['Body'].read().decode('utf-8')

    # load the json string into the python dictionary
    json_data = json.loads(json_string)

    # print the JSON Data
    print(json.dumps(json_data, indent=4))

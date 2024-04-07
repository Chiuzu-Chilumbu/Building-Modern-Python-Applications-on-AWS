"""
This module demonstrates how to use boto3 to acces and AWS services through:
resource : higher-level object-oriented service acess
"""
import boto3
import json


def access_s3_bucket(bucket_name):
    """this function provides access to an s3 bucket based on its name and shows the content stored in it"""
    #  create an S3 resource
    s3 = boto3.resource('s3')

    # Retrieve the bucket object
    bucket = s3.Bucket(bucket_name)

    # obtain all objects available in th bucket, as a collection
    for obj in bucket.objects.all():
        print(obj.key, obj.last_modified)



def access_s3_bucket_file_data(bucket_name, file_name):
    """print the contents of the json file stored in the s3 bucket"""

    #  create an S3 resource
    s3 = boto3.resource('s3')

    # Retrieve the bucket object
    bucket = s3.Bucket(bucket_name)

    # Retrieve the object (file) from the bucket
    obj = bucket.Object(file_name)

    #  Read the file's content into a string
    json_string = obj.get()['Body'].read().decode('utf-8')

    #  parse the JSON string into a python dictionary
    json_data = json.loads(json_string)

    #  print the json data
    print(json.dumps(json_data, indent=4))
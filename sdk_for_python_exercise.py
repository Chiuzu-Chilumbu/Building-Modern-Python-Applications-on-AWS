"""
In this module we will use python to :
  1. Create an S3 bucket for storage and hosting
  2. List all the S3 buckets 
  3. Upload content to the S3 bucket
"""


import os
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3', 'ap-northeast-3')


def create_s3_bucket(bucket_name, region='ap-northeast-3'):
    """Create an S3 bucket in a specified region."""
    try:
        location = {'LocationConstraint': region}
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        print(f"Bucket {bucket_name} created successfully.")
    except ClientError as e:
        print(f"An error occurred: {e}")


def list_all_buckets():
    """list buckets"""
    try:
        response = s3.list_buckets()
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(f' {bucket["Name"]}')
    except ClientError as e:
        print(f"An error occured {e}")


def upload_data_files(selected_bucket_name, selected_file_name):
    """upload data file"""
    cwd = os.getcwd()
    
    print(f"uploading {selected_file_name} to {selected_bucket_name}")
    
    try:
        s3.upload_file(os.path.join(cwd, selected_file_name), selected_bucket_name, selected_file_name)
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.Bucket(selected_bucket_name)
        
		# objects are stored as collection in the bucket object
        for obj in bucket.objects.all():
            print(obj.key, obj.last_modified)
    
    except ClientError as e:
        print(f"An error occured {e}")
        

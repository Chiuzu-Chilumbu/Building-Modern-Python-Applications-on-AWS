"""This module contains a series of commands needed to upload the listDragons method to AWS lambda"""


from invoke import task
import os

@task
def put_parameters(c):
    """Add SSM parameters for the bucket name and file name"""
    c.run('aws ssm put-parameter --name "dragon_data_bucket_name" --value "your-bucket-name" --type "String"')
    c.run('aws ssm put-parameter --name "dragon_data_file_name" --value "your-file-name.json" --type "String"')

@task
def set_role_arns(c):
    """Set environment variables for the IAM role ARNs"""
    readwrite_role_arn = c.run('aws iam get-role --role-name dragons-readwrite-lambda-role --query "Role.Arn" --output text', hide=True).stdout.strip()
    read_role_arn = c.run('aws iam get-role --role-name dragons-read-lambda-role --query "Role.Arn" --output text', hide=True).stdout.strip()
    os.environ['ROLE_ARN_READWRITE'] = readwrite_role_arn
    os.environ['ROLE_ARN_READ'] = read_role_arn
    print(f"ROLE_ARN_READ: {read_role_arn}")
    print(f"ROLE_ARN_READWRITE: {readwrite_role_arn}")

@task
def zip_packages(c):
    """Zip the packages and function code"""
    c.run('zip -r ../pythonlistDragonsFunction.zip .', echo=True, cwd='package')
    c.run('zip -g pythonlistDragonsFunction.zip listDragons.py', echo=True)

@task
def create_lambda_function(c):
    """Create the Lambda function"""
    role_arn_read = os.getenv('ROLE_ARN_READ')
    c.run(f'aws lambda create-function --function-name ListDragons '
          f'--runtime python3.9 '
          f'--role {role_arn_read} '
          f'--handler listDragons.listDragons '
          f'--publish '
          f'--zip-file fileb://pythonlistDragonsFunction.zip', echo=True)

@task
def invoke_lambda_function(c):
    """Invoke the Lambda function"""
    c.run('aws lambda invoke --function-name ListDragons output.txt', echo=True)



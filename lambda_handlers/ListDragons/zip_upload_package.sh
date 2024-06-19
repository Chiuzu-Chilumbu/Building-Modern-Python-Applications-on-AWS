#!/bin/bash -x

# List the contents of the ListDragons directory
ls ~/python-dragons-lambda/ListDragons/

# Navigate to the ListDragons directory
cd ~/python-dragons-lambda/ListDragons

# Install the AWS X-Ray SDK in the package directory
pip3 install -t package aws-xray-sdk

# Create a new .zip package for the updated ListDragons function
cd package
zip -r ../pythonlistDragonsFunction.zip .
cd ..
zip -g pythonlistDragonsFunction.zip listDragons.py

# Update the Lambda function code
aws lambda update-function-code --function-name ListDragons --zip-file fileb://pythonlistDragonsFunction.zip

# Enable active tracing for the Lambda function
aws lambda update-function-configuration --function-name ListDragons --tracing-config Mode=Active

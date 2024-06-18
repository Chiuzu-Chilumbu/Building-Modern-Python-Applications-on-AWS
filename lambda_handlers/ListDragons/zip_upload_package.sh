#!/bin/bash -x

# This script zips and uploads the lambda handler package to AWS Lambda

# Define variables
PACKAGE_DIR="package"
ZIP_FILE="pythonlistDragonsFunction.zip"
LAMBDA_FUNCTION_NAME="ListDragons"
PYTHON_FILE="listDragons.py"
ROLE_ARN_READ="arn:aws:iam::123456789012:role/lambda-ex" # Example lambda role ARN

# Step 1: Install boto3 package into the package directory
echo "Installing boto3 package..."
pip3 install -t $PACKAGE_DIR boto3

# Step 2: Navigate to the package directory
cd $PACKAGE_DIR

# Step 3: Zip the contents of the package directory
echo "Zipping the package directory..."
zip -r ../$ZIP_FILE .

# Step 4: Navigate back to the original directory
cd ..

# Step 5: Add the Python file to the zip archive
echo "Adding Python file to the zip archive..."
zip -g $ZIP_FILE $PYTHON_FILE

# Step 6: Create the AWS Lambda function
echo "Creating AWS Lambda function..."
aws lambda create-function --function-name $LAMBDA_FUNCTION_NAME \
--runtime python3.9 \
--role $ROLE_ARN_READ \
--handler listDragons.listDragons \
--publish \
--zip-file fileb://$ZIP_FILE

# Step 7: Invoke the AWS Lambda function
echo "Invoking AWS Lambda function..."
aws lambda invoke --function-name $LAMBDA_FUNCTION_NAME output.txt

echo "Process completed."

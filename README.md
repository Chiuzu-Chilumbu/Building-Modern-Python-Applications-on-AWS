# Building Modern Python Applications on AWS

Welcome to my project for the edX course, "Building Modern Python Applications on AWS".

![Final Architecture](images/FinalArchitecture.png) 

## Final Architecture

The diagram above illustrates the final architecture of the project. It shows how different AWS services like Lambda, API Gateway, S3, Step Functions, and others integrate to form a complete serverless application. Here's a brief overview:

- **Amazon API Gateway**: Serves as the entry point for the application, managing and routing incoming requests.
- **AWS Lambda**: Contains the business logic, with functions like `listDragons` for retrieving data and `validateDragon` & `addDragon` for processing new entries.
- **Amazon S3**: Used for storing persistent data, such as a database of dragons or user-uploaded content.
- **AWS Step Functions**: Orchestrates the workflow between different Lambda functions, especially in handling more complex operations like adding new dragons.
- **Parameter Store**: Manages configuration data and secrets, ensuring secure access to vital application parameters.
- **Amazon SNS**: Facilitates message broadcasting and subscription, useful for notifications regarding failures and success when adding new dragons.

For more information and details about the course, you can find all helpful content here: [EDX Course Link](https://learning.edx.org/course/course-v1:AWS+OTP-AWSD12+1T2022a/home)

## My Contributions

### Postman Integration Tests

I have integrated Postman tests to ensure the API endpoints are functioning correctly. These tests cover:

- **GET Requests**: Validating idempotent and safe retrieval of data.
- **POST Requests**: Ensuring new dragon entries are created successfully, with unique data generation for each test run.
- **Response Validation**: Verifying the presence of expected attributes in the JSON response and ensuring the Lambda functions execute correctly.

### Python Pytest Tests

In addition to Postman tests, I have implemented Python pytest tests to validate the business logic within the Lambda functions. These tests include:

- **Unit Tests**: Testing individual functions to ensure they perform as expected.
- **Integration Tests**: Verifying that the interaction between different components, such as Lambda functions and S3, is working seamlessly.
- **Mocking AWS Services**: Using libraries like `moto` to simulate AWS services and test the code in isolation.

### Continuous Integration (CI) Pipeline

To ensure continuous quality and seamless integration, I have set up a CI pipeline that runs with every commit. This pipeline includes:

- **Linting**: Checking the code for syntax and style errors using tools like `autopep8`.
- **Unit Testing**: Running all pytest tests to validate the functionality.
- **Integration Testing**: Executing Postman tests to ensure API endpoints are functional.

### Final Architecture Overview

- **Amazon API Gateway**: Routes requests to the appropriate Lambda functions.
- **AWS Lambda**: Executes the business logic, including `listDragons`, `validateDragon`, and `addDragon`.
- **Amazon S3**: Stores data persistently.
- **AWS Step Functions**: Manages complex workflows.
- **Parameter Store**: Stores configuration data securely.
- **Amazon SNS**: Sends notifications for various events.

By integrating Postman tests, Python pytest tests, and a CI pipeline, I have ensured that the application is reliable, maintainable, and scalable. This approach not only enhances the development workflow but also ensures the highest quality of the software.

# MQTT DynamoDB Sensor Data Storage

This solution utilizes AWS Lambda and DynamoDB to store sensor data transmitted by IoT devices. The Lambda function processes data events containing sensor type and value, saving this information in a DynamoDB table with a composite key (timestamp and sensor type). If the table for a specific machine doesn't exist, it is created.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Overview

- Checks if the DynamoDB table for the machine exists; creates it if not.
- Receives events containing sensor type and value.
- Saves the sensor data in DynamoDB with a composite key (timestamp and sensor type).

## Prerequisites

Ensure that you have the necessary AWS credentials set up to interact with DynamoDB and Lambda.

## Setup

1. **DynamoDB Table Creation:**

   - The Lambda function creates a DynamoDB table for each machine's sensor data.
   - Ensure the Lambda function has appropriate IAM permissions to create DynamoDB tables.

2. **Lambda Function Deployment:**

   - Deploy the Lambda function for sensor data storage.
   - Set the appropriate DynamoDB table prefix in the `DYNAMODB_TABLE_PREFIX` variable.

## Usage

Invoke the Lambda function with an event containing the following parameters:

- `type`: Sensor type
- `value`: Sensor value
- `machine_id`: Identifier for the source machine

## Environment Variables

DYNAMODB_TABLE_PREFIX = 'dynamodb_table_prefix'

Customize the DYNAMODB_TABLE_PREFIX variable by either setting it as an Environment Variable in the Lambda console or directly modifying the code with your desired bucket name.

## Dependencies

- `boto3`: AWS SDK for Python

## Contributing

Feel free to contribute by reporting issues or submitting pull requests. See the [Contribution Guidelines](CONTRIBUTING.md) for more details.

## License

This DynamoDB Picture Assembly System is licensed under the [MIT License](LICENSE).

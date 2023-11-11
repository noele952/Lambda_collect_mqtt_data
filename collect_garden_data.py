import boto3
import json
from datetime import datetime
from decimal import Decimal

DYNAMODB_TABLE_PREFIX = 'dynamodb_table_prefix'

dynamodb = boto3.resource('dynamodb')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    data_type = event['type']
    data_value = event['value']
    machine_id = event['machine_id']
    
    # Check if DynamoDB table exists, create if not
    create_dynamodb_table(f'{DYNAMODB_TABLE_PREFIX}-{machine_id}')

    # Save the message in DynamoDB
    save_to_dynamodb(f'{DYNAMODB_TABLE_PREFIX}-{machine_id}', data_type, data_value)


def create_dynamodb_table(table_name):
    # Check if the table exists
    existing_tables = dynamodb.meta.client.list_tables()['TableNames']
    
    if table_name not in existing_tables:
        # Create the DynamoDB table
        try:
            table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {'AttributeName': 'timestamp', 'KeyType': 'HASH'},
                    {'AttributeName': 'sensor_type', 'KeyType': 'RANGE'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'timestamp', 'AttributeType': 'S'},
                    {'AttributeName': 'sensor_type', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5,
                }
            )
            
            # Wait for the table to be created
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        except dynamodb.meta.client.exceptions.ResourceInUseException:
            # Table is already being created, wait for it to exist
            dynamodb.meta.client.get_waiter('table_exists').wait(TableName=table_name)


def save_to_dynamodb(table_name, sensor_type, sensor_value):
    # Generate timestamp and save the sensor reading in DynamoDB with a composite key
    timestamp = datetime.now().isoformat()
    
    # Convert float to Decimal
    sensor_value_decimal = Decimal(str(sensor_value))
    
    table = dynamodb.Table(table_name)
    table.put_item(Item={
        'timestamp': timestamp,
        'sensor_type': sensor_type,
        'sensor_value': sensor_value_decimal
    })

import boto3
import os

# Table configuration
TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'dev-promodeagro-procurement-purchaseOrderTable')
REGION = os.environ.get('AWS_REGION', 'ap-south-1')

dynamodb = boto3.client('dynamodb', region_name=REGION)

def create_table():
    try:
        response = dynamodb.create_table(
            TableName=TABLE_NAME,
            AttributeDefinitions=[
                {'AttributeName': 'poNumber', 'AttributeType': 'S'},
                {'AttributeName': 'type', 'AttributeType': 'S'},
            ],
            KeySchema=[
                {'AttributeName': 'poNumber', 'KeyType': 'HASH'},
            ],
            BillingMode='PAY_PER_REQUEST',
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'TypeIndex',
                    'KeySchema': [
                        {'AttributeName': 'type', 'KeyType': 'HASH'},
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    }
                }
            ]
        )
        print(f"Table creation initiated: {response['TableDescription']['TableName']}")
    except dynamodb.exceptions.ResourceInUseException:
        print(f"Table '{TABLE_NAME}' already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")

def main():
    create_table()

if __name__ == "__main__":
    main() 
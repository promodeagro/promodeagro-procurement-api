import boto3
import os
import logging
from botocore.exceptions import ClientError

# Configure logging for better debugging and monitoring
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DynamoDB:
    """A wrapper class for DynamoDB operations."""
    
    def __init__(self, table_name=None):
        """
        Initializes the DynamoDB resource and table.
        If table_name is not provided, it fetches it from the 'DYNAMODB_TABLE' environment variable.
        """
        try:
            self.dynamodb = boto3.resource('dynamodb')
            if table_name:
                self.table_name = table_name
            else:
                self.table_name = os.environ.get('DYNAMODB_TABLE')

            if not self.table_name:
                raise ValueError("DYNAMODB_TABLE environment variable not set or table_name not provided.")
            
            self.table = self.dynamodb.Table(self.table_name)
            logger.info(f"Successfully connected to DynamoDB table: {self.table_name}")
        except Exception as e:
            logger.error(f"Error initializing DynamoDB client: {e}")
            raise

    def put_item(self, item):
        """
        Puts an item into the DynamoDB table.
        :param item: A dictionary representing the item.
        :return: The response from DynamoDB.
        """
        try:
            response = self.table.put_item(Item=item)
            logger.info(f"Successfully put item: {item.get('pk')}")
            return response
        except ClientError as e:
            logger.error(f"Error putting item {item.get('pk')}: {e.response['Error']['Message']}")
            raise

    def get_item(self, key):
        """
        Gets an item from the DynamoDB table by its key.
        :param key: A dictionary representing the primary key.
        :return: The item dictionary or None if not found.
        """
        try:
            response = self.table.get_item(Key=key)
            item = response.get('Item')
            if item:
                logger.info(f"Successfully retrieved item with key: {key}")
            else:
                logger.warning(f"No item found with key: {key}")
            return item
        except ClientError as e:
            logger.error(f"Error getting item with key {key}: {e.response['Error']['Message']}")
            raise

    def update_item(self, key, update_expression, expression_attribute_values, expression_attribute_names=None, condition_expression=None):
        """
        Updates an item in the DynamoDB table.
        :param key: The primary key of the item to update.
        :param update_expression: Defines the attributes to be updated.
        :param expression_attribute_values: Dictionary of values used in the update expression.
        :param expression_attribute_names: Dictionary of name substitutions for attributes.
        :param condition_expression: A condition that must be met for the update to occur.
        :return: The updated attributes of the item.
        """
        try:
            params = {
                'Key': key,
                'UpdateExpression': update_expression,
                'ExpressionAttributeValues': expression_attribute_values,
                'ReturnValues': "UPDATED_NEW"
            }
            if expression_attribute_names:
                params['ExpressionAttributeNames'] = expression_attribute_names
            if condition_expression:
                params['ConditionExpression'] = condition_expression

            response = self.table.update_item(**params)
            logger.info(f"Successfully updated item with key: {key}")
            return response.get('Attributes')
        except ClientError as e:
            logger.error(f"Error updating item with key {key}: {e.response['Error']['Message']}")
            raise

    def delete_item(self, key):
        """
        Deletes an item from the DynamoDB table.
        :param key: The primary key of the item to delete.
        :return: The response from DynamoDB.
        """
        try:
            response = self.table.delete_item(Key=key)
            logger.info(f"Successfully deleted item with key: {key}")
            return response
        except ClientError as e:
            logger.error(f"Error deleting item with key {key}: {e.response['Error']['Message']}")
            raise

    def query(self, **kwargs):
        """
        Queries the table using a key condition expression.
        :param kwargs: Keyword arguments for the query operation (e.g., KeyConditionExpression).
        :return: A list of items matching the query.
        """
        try:
            response = self.table.query(**kwargs)
            items = response.get('Items', [])
            logger.info(f"Query returned {len(items)} items.")
            
            # Handle pagination if there are more items
            while 'LastEvaluatedKey' in response:
                kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
                response = self.table.query(**kwargs)
                items.extend(response.get('Items', []))
                logger.info(f"Paginated query returned {len(response.get('Items', []))} more items.")

            return items
        except ClientError as e:
            logger.error(f"Error querying table: {e.response['Error']['Message']}")
            raise
            
    def scan(self, **kwargs):
        """
        Scans the entire table. Use sparringly as it can be inefficient.
        :param kwargs: Keyword arguments for the scan operation (e.g., FilterExpression).
        :return: A list of all items in the table.
        """
        try:
            response = self.table.scan(**kwargs)
            items = response.get('Items', [])
            logger.info(f"Scan returned {len(items)} items.")

            # Handle pagination
            while 'LastEvaluatedKey' in response:
                kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
                response = self.table.scan(**kwargs)
                items.extend(response.get('Items', []))
                logger.info(f"Paginated scan returned {len(response.get('Items', []))} more items.")
            
            return items
        except ClientError as e:
            logger.error(f"Error scanning table: {e.response['Error']['Message']}")
            raise 
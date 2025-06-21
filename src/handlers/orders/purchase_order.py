import json
import logging
import uuid
from datetime import datetime

from src.commonfunctions.dynamodb import DynamoDB
from src.commonfunctions.response import api_response

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

db = DynamoDB()
PO_TYPE = "PurchaseOrder"

def create(event, context):
    """Handles the creation of a new purchase order."""
    try:
        body = json.loads(event.get('body', '{}'))
        
        # Basic validation
        if not all(k in body for k in ['supplierName', 'deliveryDate', 'items']):
            return api_response(400, {"message": "Missing required fields"})

        po_number = f"PO-{uuid.uuid4().hex[:6].upper()}"
        
        item = {
            'poNumber': po_number,
            'type': PO_TYPE,
            'status': 'Draft',
            'orderDate': datetime.utcnow().isoformat(),
            **body
        }
        
        db.put_item(item)
        return api_response(201, item)
        
    except Exception as e:
        logger.error(f"Error creating purchase order: {e}")
        return api_response(500, {"message": "Internal Server Error"})

def list(event, context):
    """Handles listing all purchase orders."""
    try:
        # Using the GSI to fetch all items of type "PurchaseOrder"
        items = db.query(
            IndexName='TypeIndex',
            KeyConditionExpression='#type = :type',
            ExpressionAttributeNames={'#type': 'type'},
            ExpressionAttributeValues={':type': PO_TYPE}
        )
        return api_response(200, {"data": items, "total": len(items)})
        
    except Exception as e:
        logger.error(f"Error listing purchase orders: {e}")
        return api_response(500, {"message": "Internal Server Error"})

def get(event, context):
    """Handles retrieving a single purchase order by its number."""
    try:
        po_number = event['pathParameters']['poNumber']
        key = {'poNumber': po_number}
        
        item = db.get_item(key)
        
        if item:
            return api_response(200, item)
        else:
            return api_response(404, {"message": "Purchase order not found"})
            
    except Exception as e:
        logger.error(f"Error getting purchase order {po_number}: {e}")
        return api_response(500, {"message": "Internal Server Error"})

def update(event, context):
    """Handles updating an existing purchase order."""
    try:
        po_number = event['pathParameters']['poNumber']
        body = json.loads(event.get('body', '{}'))
        
        key = {'poNumber': po_number}

        # Construct update expression
        update_expression = "SET "
        expression_attribute_values = {}
        expression_attribute_names = {}
        
        for i, (k, v) in enumerate(body.items()):
            # Don't allow updating poNumber or type
            if k not in ['poNumber', 'type']:
                attr_name_placeholder = f"#attr{i}"
                attr_value_placeholder = f":val{i}"
                update_expression += f"{attr_name_placeholder} = {attr_value_placeholder}, "
                expression_attribute_names[attr_name_placeholder] = k
                expression_attribute_values[attr_value_placeholder] = v

        # Remove trailing comma and space
        update_expression = update_expression.strip(", ")

        if not expression_attribute_values:
             return api_response(400, {"message": "No fields to update"})

        updated_item = db.update_item(
            key=key,
            update_expression=update_expression,
            expression_attribute_names=expression_attribute_names,
            expression_attribute_values=expression_attribute_values
        )
        
        return api_response(200, updated_item)

    except Exception as e:
        logger.error(f"Error updating purchase order {po_number}: {e}")
        return api_response(500, {"message": "Internal Server Error"})

def delete(event, context):
    """Handles deleting a purchase order."""
    try:
        po_number = event['pathParameters']['poNumber']
        key = {'poNumber': po_number}
        
        db.delete_item(key)
        
        return api_response(204, {})
        
    except Exception as e:
        logger.error(f"Error deleting purchase order {po_number}: {e}")
        return api_response(500, {"message": "Internal Server Error"})

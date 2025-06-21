import json
import decimal

def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj

def api_response(status_code, body):
    """
    Creates a standard API Gateway response.
    :param status_code: The HTTP status code.
    :param body: The response body, which will be serialized to JSON.
    :return: A dictionary formatted for API Gateway.
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  #
        },
        "body": json.dumps(convert_decimal(body))
    } 
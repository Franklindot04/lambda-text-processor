import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TextProcessingResults')

# Structured logging helper
def log(level, message, request_id=None, **details):
    entry = {
        "level": level,
        "message": message,
        "requestId": request_id,
        "details": details
    }
    print(json.dumps(entry))

# Convert DynamoDB Decimals to int/float
def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    if isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj


def lambda_handler(event, context):
    request_id = context.aws_request_id
    log("INFO", "Received request for single result", request_id, event=event)

    try:
        # Extract ID from path parameters
        record_id = event.get("pathParameters", {}).get("id")
        if not record_id:
            log("ERROR", "Missing ID in path", request_id)
            return {
                "statusCode": 400,
                "headers": cors_headers(),
                "body": json.dumps({"error": "Missing ID in path"})
            }

        log("INFO", "Fetching item", request_id, id=record_id)

        response = table.get_item(Key={"id": record_id})
        item = response.get("Item")

        if not item:
            log("INFO", "Item not found", request_id, id=record_id)
            return {
                "statusCode": 404,
                "headers": cors_headers(),
                "body": json.dumps({"error": "Item not found"})
            }

        # Convert Decimal fields
        item = convert_decimals(item)

        log("INFO", "Item fetched successfully", request_id, id=record_id)

        return {
            "statusCode": 200,
            "headers": cors_headers(),
            "body": json.dumps(item)
        }

    except Exception as e:
        log("ERROR", "Unhandled exception while fetching result", request_id, error=str(e))
        return {
            "statusCode": 500,
            "headers": cors_headers(),
            "body": json.dumps({"error": "Internal server error"})
        }


def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }


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
        # Convert to int if no decimal places, else float
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj


def lambda_handler(event, context):
    request_id = context.aws_request_id
    log("INFO", "Received request for all results", request_id, event=event)

    try:
        response = table.scan()
        items = response.get("Items", [])

        # Convert DynamoDB Decimal types
        items = convert_decimals(items)

        log("INFO", "Fetched results successfully", request_id, count=len(items))

        return {
            "statusCode": 200,
            "headers": cors_headers(),
            "body": json.dumps(items)
        }

    except Exception as e:
        log("ERROR", "Unhandled exception while listing results", request_id, error=str(e))
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


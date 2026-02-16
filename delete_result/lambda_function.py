import json
import boto3

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


def lambda_handler(event, context):
    request_id = context.aws_request_id
    log("INFO", "Received delete request", request_id, event=event)

    try:
        # Extract ID from path
        record_id = event.get("pathParameters", {}).get("id")
        if not record_id:
            log("ERROR", "Missing ID in path", request_id)
            return {
                "statusCode": 400,
                "headers": cors_headers(),
                "body": json.dumps({"error": "Missing ID in path"})
            }

        log("INFO", "Checking if item exists", request_id, id=record_id)

        # Check if item exists
        response = table.get_item(Key={"id": record_id})
        item = response.get("Item")

        if not item:
            log("INFO", "Item not found, cannot delete", request_id, id=record_id)
            return {
                "statusCode": 404,
                "headers": cors_headers(),
                "body": json.dumps({"error": "Item not found"})
            }

        # Delete the item
        table.delete_item(Key={"id": record_id})
        log("INFO", "Item deleted successfully", request_id, id=record_id)

        return {
            "statusCode": 200,
            "headers": cors_headers(),
            "body": json.dumps({"message": "Item deleted successfully"})
        }

    except Exception as e:
        log("ERROR", "Unhandled exception while deleting item", request_id, error=str(e))
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


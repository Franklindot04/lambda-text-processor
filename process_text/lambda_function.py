import json
import time
import uuid
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
    log("INFO", "Received event", request_id, event=event)

    try:
        # Parse JSON body
        try:
            body = json.loads(event.get("body", "{}"))
        except json.JSONDecodeError:
            log("ERROR", "Invalid JSON", request_id)
            return error_response(400, "Invalid JSON")

        # Validate required field
        if "text" not in body:
            log("ERROR", "Missing 'text' field", request_id)
            return error_response(400, "Missing required field: text")

        text = body["text"]

        # Validate type
        if not isinstance(text, str):
            log("ERROR", "Text is not a string", request_id, received_type=str(type(text)))
            return error_response(400, "Field 'text' must be a string")

        # Validate non-empty
        if text.strip() == "":
            log("ERROR", "Text is empty", request_id)
            return error_response(400, "Field 'text' cannot be empty")

        # Build result object
        result = {
            "id": str(uuid.uuid4()),
            "original": text,
            "uppercase": text.upper(),
            "length": len(text),
            "timestamp": int(time.time())
        }

        # Store in DynamoDB
        table.put_item(Item=result)
        log("INFO", "Item stored successfully", request_id, id=result["id"])

        return success_response(result)

    except Exception as e:
        log("ERROR", "Unhandled exception", request_id, error=str(e))
        return error_response(500, "Internal server error")


def success_response(body):
    return {
        "statusCode": 200,
        "headers": cors_headers(),
        "body": json.dumps(body)
    }


def error_response(status, message):
    return {
        "statusCode": status,
        "headers": cors_headers(),
        "body": json.dumps({"error": message})
    }


def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }


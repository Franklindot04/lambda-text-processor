import json
import uuid
import time
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TextProcessingResults')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    text = body.get('text', '')

    result = {
        'id': str(uuid.uuid4()),
        'original': text,
        'uppercase': text.upper(),
        'length': len(text),
        'timestamp': int(time.time())
    }

    table.put_item(Item=result)

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }

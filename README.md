# 🚀 Text Processing Serverless API

![AWS](https://img.shields.io/badge/AWS-Lambda-orange?logo=amazonaws)
![API Gateway](https://img.shields.io/badge/AWS-API_Gateway-yellow?logo=amazonaws)
![DynamoDB](https://img.shields.io/badge/AWS-DynamoDB-blue?logo=amazonaws)
![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)
![IaC Ready](https://img.shields.io/badge/Infrastructure-CDK/Terraform_ready-green)
![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen)

A fully serverless CRUD API built using **AWS Lambda**, **API Gateway**, and **DynamoDB**.  
Designed with clean architecture, structured logging, and production‑grade error handling.

---

# 📸 Screenshots

> Add your screenshots here once you take them.  
> Suggested screenshots:
- API Gateway routes  
- DynamoDB table with items  
- CloudWatch logs showing structured JSON  
- Successful POST / GET / DELETE responses in terminal  

Example placeholder:

/screenshots/
api-gateway-routes.png
dynamodb-table.png
cloudwatch-logs.png
curl-tests.png

---

# 🏗 Architecture Overview

## High-Level Architecture Diagram

┌──────────────────────────┐
│      API Gateway         │
│  (REST Endpoints Layer)  │
└─────────────┬────────────┘
│
┌────────────────────────┼────────────────────────┐
│                        │                        │
┌──────────┐           ┌──────────────┐         ┌──────────────┐
│ POST /   │           │ GET /results │         │ GET /results/ │
│process   │           │   (list)     │         │     {id}      │
└────┬─────┘           └──────┬───────┘         └──────┬───────┘
│                        │                        │
▼                        ▼                        ▼
┌──────────┐           ┌──────────────┐         ┌──────────────┐
│ Lambda   │           │ Lambda       │         │ Lambda       │
│Process   │           │ListResults   │         │GetResult     │
└────┬─────┘           └──────┬───────┘         └──────┬───────┘
│                        │                        │
└──────────────┬─────────┴──────────┬────────────┘
▼                    ▼
┌──────────────────────────────┐
│     DynamoDB Table           │
│  TextProcessingResults       │
└──────────────────────────────┘

---

## Sequence Diagram (POST → DynamoDB)

Client
│
│ POST /
▼
API Gateway
│
│ invokes Lambda
▼
ProcessTextFunction
│
│ put_item()
▼
DynamoDB
│
│ success
▼
ProcessTextFunction
│
│ returns JSON
▼
Client

---

# 🌐 Base URL

https://3ki380u3fc.execute-api.eu-north-1.amazonaws.com

---

# 📚 API Documentation

## 🔵 POST `/`

Process text and store the result.

### Request

```json
{
  "text": "hello world"
}
{
  "id": "uuid",
  "original": "hello world",
  "uppercase": "HELLO WORLD",
  "length": 11,
  "timestamp": 1771283745
}
🟢 GET /results
List all stored results.

Response
[
  {
    "id": "uuid",
    "original": "hello",
    "uppercase": "HELLO",
    "length": 5,
    "timestamp": 1771283745
  }
]
🟡 GET /results/{id}
Retrieve a single result by ID.

Example
GET /results/f5e565d8-bc1f-4911-a810-e1c3e06d8c98
Response
{
  "id": "f5e565d8-bc1f-4911-a810-e1c3e06d8c98",
  "original": "hello",
  "uppercase": "HELLO",
  "length": 5,
  "timestamp": 1771283745
}

🔴 DELETE /results/{id}
Delete a result by ID.

Example

DELETE /results/f5e565d8-bc1f-4911-a810-e1c3e06d8c98

Response

{ "message": "Item deleted successfully" }

🛡 CORS
All responses include:

{
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET,POST,DELETE,OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type"
}

🗄 DynamoDB Schema
Table: TextProcessingResults

Attribute	Type
id	String (PK)
original	String
uppercase	String
length	Number
timestamp	Number

📊 Logging Strategy
Every Lambda uses structured JSON logs:

{
  "level": "INFO",
  "message": "Item stored successfully",
  "requestId": "abc-123",
  "details": { "id": "uuid" }
}

This makes CloudWatch logs:

searchable

filterable

machine‑readable

consistent across all Lambdas

🛠 Deployment
From each Lambda folder:

zip function.zip lambda_function.py
aws lambda update-function-code \
  --function-name <LambdaName> \
  --zip-file fileb://function.zip

🧪 Local Testing
POST

curl -X POST https://3ki380u3fc.execute-api.eu-north-1.amazonaws.com/ \
  -H "Content-Type: application/json" \
  -d '{"text": "hello"}'

GET all

curl https://3ki380u3fc.execute-api.eu-north-1.amazonaws.com/results

GET one

curl https://3ki380u3fc.execute-api.eu-north-1.amazonaws.com/results/<id>

DELETE

curl -X DELETE https://3ki380u3fc.execute-api.eu-north-1.amazonaws.com/results/<id>

🚧 Future Improvements
Add authentication (Cognito / JWT)

Add pagination to /results

Add update endpoint (PATCH)

Add frontend UI (React or Svelte)

Add CloudFormation / CDK deployment

🎉 Final Notes
This project demonstrates:

clean serverless architecture

modular Lambda design

consistent logging

DynamoDB best practices

production‑grade error handling

Perfect for showcasing DevOps + backend engineering skills.



import json
import boto3


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("RestaurantOrders")


def lambda_handler(event, context):
    scan = table.scan()
    items = scan.get("Items", [])
    for item in items:
        item["quantity"] = int(item["quantity"])
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(items)
    }

lambda_handler(None, None)
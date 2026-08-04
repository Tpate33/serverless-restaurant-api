import json
import boto3


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("RestaurantOrders")


def lambda_handler(event, context):
    path_parameters = event.get("pathParameters") or {}
    order_id = path_parameters.get("orderId")

    if not order_id:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "orderId is required"
            })
        }

    response = table.get_item(
        Key={
            "orderId": order_id
        }
    )

    print(response)

    order = response.get("Item")

    if order is None:
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": f"Order with ID {order_id} not found"
            })
        }

    order["quantity"] = int(order["quantity"])

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(order)
    }

test_event = {
    "pathParameters": {
        "orderId": "c48e3fbf-4d9b-4390-93c59be11275c8f"
    }
}

print(lambda_handler(test_event, None))
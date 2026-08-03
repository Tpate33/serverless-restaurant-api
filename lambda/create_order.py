import json
import uuid
import boto3



dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("RestaurantOrders")


def lambda_handler(event, context):
    """
    Validate a restaurant order and return an API-style response.

    Expected event format:
    {
        "customerName": "Ahmed",
        "item": "Cheese Pizza",
        "quantity": 2
    }
    """
    body = json.loads(event.get("body"))

    # Safely retrieve each value from the incoming request.
    # .get() returns None when a key is missing.
    customer_name = body.get("customerName")
    item = body.get("item")
    quantity = body.get("quantity")

    # Validate the customer's name.
    if customer_name is None:
        return {
            "statusCode": 400,
            "body": "customerName is required"
        }

    if type(customer_name) is not str:
        return {
            "statusCode": 400,
            "body": "customerName must be text"
        }

    if customer_name.strip() == "":
        return {
            "statusCode": 400,
            "body": "customerName cannot be empty"
        }

    # Validate the ordered item.
    if item is None:
        return {
            "statusCode": 400,
            "body": "item is required"
        }

    if type(item) is not str:
        return {
            "statusCode": 400,
            "body": "item must be text"
        }

    if item.strip() == "":
        return {
            "statusCode": 400,
            "body": "item cannot be empty"
        }

    # Validate the quantity.
    if quantity is None:
        return {
            "statusCode": 400,
            "body": "quantity is required"
        }

    if type(quantity) is not int:
        return {
            "statusCode": 400,
            "body": "quantity must be a number"
        }

    if quantity <= 0:
        return {
            "statusCode": 400,
            "body": "quantity must be greater than 0"
        }


    

    # Remove unnecessary spaces before using the values.
    customer_name = customer_name.strip()
    item = item.strip()

    order_id = str(uuid.uuid4())

    order = {
        "orderId": order_id,
        "customerName": customer_name,
        "item": item,
        "quantity": quantity

    }

    response = table.put_item(Item=order)    
    print(response)
    
    return {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "orderId": order_id,
            "customerName": customer_name,
            "item": item,
            "quantity": quantity
        })
    }

    
    
    
    # Return a successful response.
    # The order is not stored in DynamoDB yet.
    # return {
    #     "statusCode": 201,
    #     "body": (
    #         f"Created order for {customer_name}: "
    #         f"{quantity} {item}"
    #     )
    # }

test_event = {
    "body": '{"customerName":"Ahmed","item":"Cheese Pizza","quantity":2}'
}

print(lambda_handler(test_event, None))
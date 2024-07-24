from fastapi import FastAPI
from fastapi import Request
import db_helper
from fastapi.responses import JSONResponse


app = FastAPI()

inprogress_orders = {}

@app.post("/")
async def handle_request(request: Request):

    payload = await request.json()

    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    intent_handler_dict = {
        'Order Complete - context :  order-ongoing': add_to_order,
        'Track order - context: ongoing-tracking': track_order
    }

    return intent_handler_dict[intent](parameters)


def add_to_order(parameters: dict):
    medicines = parameters.get("Medicines", [])
    quantity = parameters.get("number", [])

    if len(medicines) != len(quantity):
        fulfillment_text = "Sorry, I didn't understand. Please specify the quantity for each medicine."
    else:
        fulfillment_text = f"Received {medicines} and {quantity} in the backend."

    return JSONResponse(content={"fulfillmentText": fulfillment_text})


def track_order(parameters: dict):
    order_id = int(parameters['number'])
    order_status = db_helper.get_order_status(order_id)

    if order_status:
        fulfilment_text = f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfilment_text = f"No order found with order id: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfilment_text
    })



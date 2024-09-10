from flask import request, Blueprint
from Helper_Order.logHandler import logger
from Helper_Order.verify_token import jwt_required
from Services_Order.order_service import *
from http import HTTPStatus
import stripe
import json
import os 


create_blueprint = Blueprint('Create_Blueprint', __name__, url_prefix='/api/v1/order')
stripe.api_key = os.getenv('STRIPE_API_KEY')


@create_blueprint.route('/create-payment-intent', methods=['POST'])
@jwt_required
def intent():
    try:
        print(f"Key for stripe is {os.getenv('STRIPE_API_KEY')}")
        customer = stripe.Customer.search(query=f"email:\"{request.get_json()['currentUser']['email']}\"")
        customer_id = ''
        if len(customer.data) == 0:
            meta_data = {
                'buyerId': request.get_json()['buyerId']
            }
            create_customer = stripe.Customer.create(email=request.get_json()['currentUser']['email'], metadata=meta_data)
            customer_id = create_customer.id
            logger.info(f"intent controller method , customer was not found creating new customer..")
        else:
            customer_id = customer.data[0]
            print(f"Customer id after else is {customer_id}")
            logger.info(f"intent controller method , customer was found ")
        if customer_id is not None:
            service_fee = (5.5 / 100) * int(request.get_json()['price']) + 2 if int(request.get_json()['price']) < 50 else (5.5 / 100) * int(request.get_json()['price'])
            payment_intent = stripe.PaymentIntent.create(amount=int(int(request.get_json()['price']) + service_fee * 100), currency='usd', customer=customer_id, automatic_payment_methods={"enabled": True})
            print(f"Payment Intent is {payment_intent}")
            logger.info(f"intent controller method , payment intent created succefully.")
        response = {
            'Message': 'Order intent Created successfully.',
            'Http Status': HTTPStatus.OK,
            'clientSecret': payment_intent['client_secret'],
            'paymentIntentId': payment_intent['id']
        }
        return response
    except Exception as err:
        logger.error(f"Error in inten controller method : {str(err)}")
        return(f"Could not Create intent Payment, please try again.")
    
    
@create_blueprint.route('/create-order', methods=['POST'])
@jwt_required
def order():
    try:
        order_data = request.get_json()
        order = createOrder(data=order_data)
        response = {
            "Message": "Order created successfully.",
            'Http Status': HTTPStatus.OK,
            "Order": order.to_mongo().to_dict(),
        }
        return(json.dumps(response, default=str))
    except Exception as err:
        logger.error(f"Error in order controller method : {str(err)}")
        return(f"Could not create new order, please try again later.")
    




# order_data = {
#             "offer": {
#                 "gigTitle": request.get_json()['gigTitle'],
#                 "price": request.get_json()['price'],
#                 "description": request.get_json()['description'],
#                 "deliveryInDays": int(request.get_json()['deliveryInDays']),
#                 "oldDeliveryDate": request.get_json()['oldDeliveryDate'],
#                 "newDeliveryDate": request.get_json()['newDeliveryDate'],
#                 "accepted": request.get_json()['accepted'],
#                 "cancelled": request.get_json()['cancelled'],
#                 "reason": request.get_json()['reason'],
#             },
#             "gigId": request.get_json()['gigId'],
#             "sellerId": request.get_json()['sellerId'],
#             "sellerUsername": request.get_json()['sellerUsername'],
#             "sellerEmail": request.get_json()['sellerEmail'],
#             "sellerImage": request.get_json()['sellerImage'],
#             "gigCoverImage": request.get_json()['gigCoverImage'],
#             "gigMainTitle": request.get_json()['gigMainTitle'],
#             "gigBasicDescription": request.get_json()['gigBasicDescription'],
#             "gigBasicTitle": request.get_json()['gigBasicTitle'],
#             "buyerId": request.get_json()['buyerId'],
#             "buyerUsername": request.get_json()['buyerUsername'],
#             "buyerEmail": request.get_json()['buyerEmail'],
#             "buyerImage": request.get_json()['buyerImage'],
#             "status": request.get_json()['status'],
#             "orderId": request.get_json()['orderId'],
#             "quantity": int(request.get_json()['quantity']),
#             "price": int(request.get_json()['order_price']),
#             "serviceFee": int(request.get_json()['serviceFee']),
#             "requirements": request.get_json()['requirements'],
#             "approved": request.get_json()['approved'],
#             "cancelled": request.get_json()['order_cancelled'],
#             "approvedAt": request.get_json()['approvedAt'],
#             "delivered": request.get_json()['delivered'],
#             "paymentIntent": request.get_json()['paymentIntent'],
#             "deliveredWork": list(request.get_json()['deliveredWork']),
#             "requestExtension": dict(request.get_json()['requestExtension']),
#             "dateOrdered": request.get_json()['dateOrdered'],
#             "buyerReview": dict(request.get_json()['buyerReview']),
#             "sellerReview": dict(request.get_json()['sellerReview']),
#             "events": {
#                 "placeOrder": request.get_json()['placeOrder'],
#                 "requirements": request.get_json()['events_requirements'],
#                 "orderStarted": request.get_json()['orderStarted'],
#                 "deliveryDateUpdate": request.get_json()['deliveryDateUpdate'],
#                 "orderDelivered": request.get_json()['orderDelivered'],
#                 "buyerReview": request.get_json()['events_buyerReview'],
#                 "sellerReview": request.get_json()['events_sellerReview'],
#             }
#         }
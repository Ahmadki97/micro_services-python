from flask import request, Blueprint
from Helper_Order.logHandler import logger
from Helper_Order.verify_token import jwt_required
from Services_Order.order_service import *
from http import HTTPStatus
import stripe
import json
import os 

update_blueprint = Blueprint('Update_Blueprint', __name__, url_prefix='/api/v1/order')
stripe.api_key = os.getenv('STRIPE_API_KEY')


@update_blueprint.route('/cancel/<string:order_id>', methods=['PUT'])
@jwt_required
def cancel(order_id: str):
    try:
        stripe.Refund.create(payment_intent=request.get_json()['paymentIntent'])
        # To refund the payment it must contain succeed charge.. not deve.opment env
        logger.info(f"Refund Done successfully for the payment intent id {request.get_json()['paymentIntent']}")
        order_data = {
            "sellerId": request.get_json()['sellerId'],
            "buyerId": request.get_json()['buyerId'],
            "purchasedGigs": request.get_json()['purchasedGigs'],
        }
        cancelOrder(order_id=order_id, data=order_data)
        response = {
            "Message": f"Order with id {order_id} canceled successfully.",
            "Http Status": HTTPStatus.OK,
        }
        return response
    except Exception as err:
        logger.error(f"Error in cancel order controller: {str(err)}")
        return(f"Could not cancel order, please try again later.")
    

@update_blueprint.route('/extension/<string:order_id>', methods=['PUT'])
@jwt_required
def requestExtension(order_id):
    try:
        order_data = {
            "originalDate": request.get_json()['originalDate'],
            "newDate": request.get_json()['newDate'],
            "days": int(request.get_json()['days']),
            "reason": request.get_json()['reason'],
        }
        order = requestDeliveryExtension(order_id=order_id, data=order_data)
        response = {
            "Message": "Request Extension sent successfully..",
            "Http Status": HTTPStatus.OK,
            "order": order.to_mongo().to_dict(),
        }
        return(json.dumps(response, default=str))
    except Exception as err:
        logger.error(f"Error in requestExtension Controller : {str(err)}")
        return(f"Could not send Extension Request please try again later.")
    

@update_blueprint.route('/gig/<string:order_id>/<string:typee>', methods=['PUT'])
@jwt_required
def deliveryDate(order_id: str, typee: str):
    try:
        if typee == 'approve':
            order_data = {
                "deliveryInDays": request.get_json()['deliveryInDays'],
                "newDeliveryDate": request.get_json()['newDeliveryDate'],
                "reason": request.get_json()['reason'],
            }
            order = approveDeliveryDate(order_id=order_id, data=order_data)
            logger.info(f"update delivery date controller, delivery date updated successfully")
        else: 
            order = rejectDeliveryDate(order_id=order_id)
            logger.info(f"update delivery date controller, delivery date rejected successfully")
        response = {
            "Message": "Order Delivery Date",
            "Http Status": HTTPStatus.OK,
            "order": order.to_mongo().to_dict(),
        }
        return(json.dumps(response, default=str))
    except Exception as err:
        logger.error(f"Error in deliveryDate Controller : {str(err)}")
        return(f"Could not send Delivery Order, please try again later.")
    

@update_blueprint.route('/approve-order/<string:order_id>', methods=['PUT'])
@jwt_required
def buyerApproveOrder(order_id: str):
    try:
        order_data = {
            "sellerId": request.get_json()['sellerId'],
            "buyerId": request.get_json()['buyerId'],
            "ongoingJobs": int(request.get_json()['ongoingJobs']),
            "completedJobs": int(request.get_json()['completedJobs']),
            "totalEarnings": int(request.get_json()['totalEarnings']),
            "purchasedGigs": request.get_json()['purchasedGigs'],
        }
        order = approveOrder(order_id=order_id, data=order_data)
        response = {
            "Message": "Order approved Successfully",
            "Http Status": HTTPStatus.OK,
            "order": order.to_mongo().to_dict(),
        }
        return(json.dumps(response, default=str))
    except Exception as err:
        logger.error(f"Error in approve order controller: {str(err)}")
        return(f"Could not approve order, please try again later.")
    

@update_blueprint.route('/deliver-order/<string:order_id>', methods=['PUT'])
@jwt_required
def deliverOrder(order_id: str):
    try:
        order_data = {
            "message": request.get_json()['message'],
            "file": request.get_json()['file'],
            "fileType": request.get_json()['fileType'],
            "fileName": request.get_json()['fileName'],
            "fileSize": request.get_json()['fileSize'],
        }
        order = sellerDeliverOrder(order_id=order_id, deliverd=True, delivered_work=order_data)
        response = {
            "Message": "Order Deliverd Successfully.",
            "Http Status": HTTPStatus.OK,
            "order": order.to_mongo().to_dict(),
        }
        return(json.dumps(response, default=str))
    except Exception as err: 
        logger.error(f"Error in delivery order Controller : {str(err)}")
        return(f"Failed to deliver order, please try again later")
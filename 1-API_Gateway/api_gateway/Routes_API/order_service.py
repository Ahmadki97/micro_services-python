from flask import request, jsonify, Blueprint
from Helper_api.requests import Requests
from Helper_api.elastic import logger
from Helper_api.errorhandlers import ServerError
from services.auth_middleware import custom_jwt_required
from dotenv import load_dotenv
import json
import os 


load_dotenv('.env')
service_url = os.getenv('ORDER_BASE_URL')
print(f"Service Url is : {service_url}")
base_url = f"{service_url}/api/v1/order"
gig_client = Requests(service_url=base_url)
order_blue_print = Blueprint('Order', __name__, url_prefix='/api/v1/order')


@order_blue_print.route('/create-order', methods=['POST'])
@custom_jwt_required
def createOrder():
    try:
        response = gig_client.makeRequest(endpoint=f"create-order", service_token='order')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in createOrder() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "createOrder() Function")
    

@order_blue_print.route('/create-payment-intent', methods=['POST'])
@custom_jwt_required
def createPaymentIntent():
    try:
        response = gig_client.makeRequest(endpoint=f"create-payment-intent", service_token='order')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in createPaymentIntent() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "createPaymentIntent() Function")
    

@order_blue_print.route('/<string:order_id>', methods=['GET'])
@custom_jwt_required
def getOrderById(order_id: str):
    try:
        response = gig_client.makeRequest(endpoint=f"{order_id}", service_token='order')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in getOrderById() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getOrderById() Function")
    

@order_blue_print.route('/seller/<string:seller_id>', methods=['GET'])
@custom_jwt_required
def getSellerOrders(seller_id: str):
    try:
        response = gig_client.makeRequest(endpoint=f"seller/{seller_id}", service_token='order')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in getsellerOrders() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getsellerOrders() Function")
    

@order_blue_print.route('/buyer/<string:buyer_id>', methods=['GET'])
@custom_jwt_required
def getBuyerOrders(buyer_id: str):
    try:
        response = gig_client.makeRequest(endpoint=f"buyer/{buyer_id}", service_token='order')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in getBuyerOrders() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getBuyerOrders() Function")
    

@order_blue_print.route('/cancel/<string:order_id>', methods=['PUT'])
@custom_jwt_required
def cancelOrder(order_id: str):
    try:
        response = gig_client.makeRequest(endpoint=f"cancel/{order_id}", service_token='order')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in cancelOrder() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "cancelOrder() Function")


@order_blue_print.route('/extension/<string:order_id>', methods=['PUT'])
@custom_jwt_required
def requestExtension(order_id: str):
    try:
        response = gig_client.makeRequest(endpoint=f"extension/{order_id}", service_token='order')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in requestExtension() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "requestExtension() Function")


@order_blue_print.route('/gig/<string:order_id>/<string:typee>', methods=['PUT'])
@custom_jwt_required
def deliveryDate(order_id: str, typee: str):
    try:
        response = gig_client.makeRequest(endpoint=f"gig/{order_id}/{typee}", service_token='order')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in deliveryDate() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "deliveryDate() Function")


@order_blue_print.route('/approve-order/<string:order_id>', methods=['PUT'])
@custom_jwt_required
def approveOrder(order_id: str):
    try:
        response = gig_client.makeRequest(endpoint=f"approve-order/{order_id}", service_token='order')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in approveOrder() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "approveOrder() Function")


@order_blue_print.route('/deliver-order/<string:order_id>', methods=['PUT'])
@custom_jwt_required
def delivereOrder(order_id: str):
    try:
        response = gig_client.makeRequest(endpoint=f"deliver-order/{order_id}", service_token='order')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in delivereOrder() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "delivereOrder() Function")





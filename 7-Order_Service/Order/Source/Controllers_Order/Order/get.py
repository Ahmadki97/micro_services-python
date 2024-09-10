from Services_Order.order_service import getOrderByBuyerId, getOrderById, getOrderBySellerId
from Helper_Order.verify_token import jwt_required
from Helper_Order.logHandler import logger
from flask import request, Blueprint
from http import HTTPStatus
import json






get_blueprint = Blueprint('Get_Blueprint', __name__, url_prefix='/api/v1/order')


@get_blueprint.route('/<string:order_id>', methods=['GET'])
@jwt_required
def orderId(order_id: str):
    try:
        order = getOrderById(order_id=order_id)
        response = {
            "Message": "Successfully Found order",
            "Http Status": HTTPStatus.OK,
            "order": order.to_mongo().to_dict()
        }
        return(json.dumps(response, default=str))
    except Exception as err:
        logger.error(f"Error in get order by id controller: {str(err)}")
        return(f"Could not get order, please try again later")
    

@get_blueprint.route('/seller/<string:seller_id>', methods=['GET'])
@jwt_required
def sellerOrders(seller_id: str):
    try:
        orders = getOrderBySellerId(seller_id=seller_id)
        response = {
            "Message": "Orders for Seller Found Successfully.",
            "Http Status": HTTPStatus.OK,
            "orders": orders
        }
        return(json.dumps(response, default=str))
    except Exception as err:
        logger.error(f"Error in get seller orders controller: {str(err)}")
        return(f"Could not get orders for seller, please try again later.")


@get_blueprint.route('/buyer/<string:buyer_id>', methods=['GET'])
@jwt_required
def buyerOrders(buyer_id: str):
    try:
        orders = getOrderByBuyerId(buyer_id=buyer_id)
        response = {
            "Message": "Orders for Buyer Found Successfully.",
            "Http Status": HTTPStatus.OK,
            "orders": orders
        }
        return(json.dumps(response, default=str))
    except Exception as err:
        logger.error(f"Error in get Buyer orders controller: {str(err)}")
        return(f"Could not get orders for buyer, please try again later.")



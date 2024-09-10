from Services_Order.notification_services import getNotificationsById
from Helper_Order.verify_token import jwt_required
from Helper_Order.logHandler import logger
from flask import request, Blueprint
from http import HTTPStatus
import json



get_notifications_blueprint = Blueprint('Get_Notifications_Blueprint', __name__, url_prefix='/api/v1/order')



@get_notifications_blueprint.route('/notification/<string:user_to>')
@jwt_required
def notification(user_to: str):
    try:
        notification = getNotificationsById(user_to_id=user_to)
        response = {
            "Message": "Notification Found Successfully.",
            "Http Status": HTTPStatus.OK,
            "notification": notification.to_dict()
        }
        return(json.dumps(response, default=str))
    except Exception as err:
        logger.error(f"Error in get notification controller: {str(err)}")
        return(f"Could not find notification, please try again later")
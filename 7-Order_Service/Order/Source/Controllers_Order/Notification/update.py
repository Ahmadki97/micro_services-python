from Services_Order.notification_services import markNotificationAsRead
from Helper_Order.verify_token import jwt_required
from Helper_Order.logHandler import logger
from flask import request, Blueprint
from http import HTTPStatus
import json



update_notification_blueprint = Blueprint('Notification_Service_Blueprint', __name__, url_prefix='/api/v1/order')


@update_notification_blueprint.route('/notification/mark-as-read', methods=['GET'])
@jwt_required
def markSingleNotificationAsRead():
    try:
        notification = markNotificationAsRead(notification_id=request.get_json()['notificationId'])
        response = {
            "Message": "Notification Marked as Read.",
            "Http Status": HTTPStatus.OK,
            "notificationId": notification.to_dict()
        }
        return(json.dumps(response, default=str))
    except Exception as err:
        logger.error(f"Error in mark single notification as read controller: {str(err)}")
        return(f"Could not mark notification as read, please try again later.")
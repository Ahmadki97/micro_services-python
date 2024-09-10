from Helper_Order.logHandler import logger
from Models_Order.notification_schema import Notification
from Sockets_Order.sockets_io import sio
import json



def createNotification(data: dict):
    try:
        notification = Notification(**data)
        notification.save()
        logger.info(f"createNotification() Method, Notification Created Successfully.")
        return notification
    except Exception as err:
        logger.error(f"Error in createNotification() Method : {str(err)}")


def getNotificationsById(user_to_id: str):
    try:
        notifications = Notification.objects.filter(userTo=user_to_id)
        logger.info(f"getNotificationsById() Method, Notifications for user {user_to_id} Found Successfully")
        notifications_list = []
        for notification in notifications:
            notifications_list.append(notification.to_mongo().to_dict())
        return notifications_list
    except Exception as err:
        logger.error(f"Error in getNotificationsById() Method: {str(err)}")


def markNotificationAsRead(notification_id: str):
    try:
        notification = Notification.objects.get(id=notification_id).modify(set__isRead=True)
        notification.reload()
        logger.info(f"markNotificationAsRead() Method, Notification with id {notification_id} marked as read.")
        from Services_Order.order_service import getOrderById
        order = getOrderById(notification.orderId)
        logger.info(f"markNotificationAsRead() Method, order with id {order.id} Found Successfully.")
        data = {
            'order': order.to_dict(),
            'notification': notification.to_dict(),
        }
        sio.emit(event='order notification', data=data)
        return notification
    except Exception as err:
        logger.error(f"Error in markNOtificationAsRead() Method : {str(err)}")


def sendNotification(data: dict, user_to_id: str, message: str):
    try:    
        notification = {
            'userTo': user_to_id,
            'senderUsername': data['sellerUsername'],
            'senderPicture': data['sellerImage'],
            'receiverUsername': data['buyerUsername'],
            'receiverPicture': data['buyerImage'],
            'message': message,
            'orderId': data['orderId'],
        }
        order_notification = createNotification(notification)
        order_notification.save()
        logger.info(f"sendNotification() Method, notification with id {order_notification.id} created successfully.")
        data_sent = {
            'data': data,
            'order': order_notification
        }
        sio.emit(event='order notification', data=json.dumps(data_sent, default=str))
        logger.info(f"Sending Data to the api Service using socketIO.")
    except Exception as err:
        logger.error(f"Error in sendNotification() Method: {str(err)}")

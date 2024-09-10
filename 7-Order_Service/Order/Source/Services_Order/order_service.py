from Helper_Order.logHandler import logger
from Models_Order.order_schema import Order
from Queues_Order.order_producer import startPublish
from Services_Order.notification_services import sendNotification
from flask import request
import datetime
import json


def getOrderById(order_id: str):
    try:
        order = Order.objects.get(orderId=order_id)
        logger.info(f"getOrderById() Method, order with id {order_id} Found Successfully.")
        return order
    except Exception as err:
        logger.error(f"Error in getOrderById() Method: {str(err)}")


def getOrderBySellerId(seller_id: str):
    try:
        orders = Order.objects.filter(sellerId=seller_id)
        # The filter return Search Query object, thats why we transform each object into document and add it to the list 
        logger.info(f"getOrderBySellerId() Method, orders for seller {seller_id} found successfully.")
        orders_list = []
        for order in orders:
            orders_list.append(order.to_mongo().to_dict())
        return orders_list
    except Exception as err:
        logger.error(f"Error in getOrderBySellerId() Method: {str(err)}")


def getOrderByBuyerId(buyer_id: str):
    try:
        orders = Order.objects.filter(buyerId=buyer_id)
        # The filter return Search Query object, thats why we transform each object into document and add it to the list 
        logger.info(f"getOrderBySellerId() Method, orders for buyer {buyer_id} found successfully.")
        orders_list = []
        for order in orders:
            orders_list.append(order.to_mongo().to_dict())
        return orders_list
    except Exception as err:
        logger.error(f"Error in getOrderBySellerId() Method: {str(err)}")



def createOrder(data: dict):
    try:
        order = Order(**data)
        order.validate()
        order.save()
        logger.info(f"createOrder() Method, order with id {order.id} created successfully.")
        message_details = {
            'sellerId': data['sellerId'],
            'count': 1,
            'type': 'create-order'
        }
        print(f"order is {order}, and the type is {type(order)}")
        startPublish(exchange_name='', routing_key='order-seller', service_name='Order', body= json.dumps(message_details))
        email_message_details = {
            'orderId': data['orderId'],
            # 'invoiceId': request.get_json()['invoiceId'],
            # 'orderDue': request.get_json()['orderDue'],
            'amount': data['price'],
            'buyerUsername': data['buyerUsername'],
            'sellerUsername': data['sellerUsername'],
            'title': data['offer']['gigTitle'],
            'description': data['offer']['description'],
            'requirements': data['requirements'],
            'serviceFee': data['serviceFee'],
            'total': order.price + order.serviceFee,
            'orderUrl': '',
            'template': ''
        }
        startPublish(exchange_name='', routing_key='order-email', service_name='Users', body= json.dumps(email_message_details))
        sendNotification(data=order.to_mongo().to_dict(), user_to_id=data['sellerUsername'], message='placed an order for your gig')
        return order
    except Exception as err:
        logger.error(f"Error in createOrder() Method: {str(err)}")


def cancelOrder(order_id: str, data: dict):
    try:
        order_new = Order.objects.get(orderId=order_id).modify(set__cancelled=True, set__status='Cancelled', set__approvedAt=datetime.datetime.now())
        order = Order.objects.get(orderId=order_id)
        logger.info(f"cancedOrder() Method,order with id {order_id} Canceleld Successfully.")
        seller_message_details = {
            'type': 'cancel-order',
            'sellerId': data['sellerId']
        }
        buyer_message_details = {
            'type': 'cancel-order',
            'buyerId': data['buyerId'],
            'purchasedGigs': data['purchasedGigs'],
        }
        startPublish(exchange_name='', routing_key='order-seller', service_name='Users', data=json.dumps(seller_message_details))
        startPublish(exchange_name='', routing_key='user-buyer', service_name='Users', data=json.dumps(buyer_message_details))
        sendNotification(data=order.to_mongo().to_dict(), user_to_id=order.sellerUsername, message='Cancelled your order Delivery')
        return order
    except Exception as err:
        logger.error(f"Error in cancelOrder() Method : {str(err)}")


def approveOrder(order_id: str, data: dict):
    try:
        order_new = Order.objects.get(orderId=order_id).modify(set__approved=True, set__status='Completed', set__approvedAt=datetime.datetime.now())
        order = Order.objects.get(orderId=order_id)
        logger.info(f"approveOrder() Method, order with id {order_id} approved successfully.")
        seller_message_details = {
            'sellerId': data['sellerId'],
            'ongoingJobs': data['ongoingJobs'],
            'completedJobs': data['completedJobs'],
            'totalEarnings': data['totalEarnings'],
            'recentDelivery': datetime.datetime.now(),
            'type': 'approve-order'
        }
        buyer_message_details = {
            'type': 'purchased-gigs',
            'buyerId': data['buyerId'],
            'purchasedGigs': data['purchasedGigs'],
        }
        startPublish(exchange_name='', routing_key='order-seller', service_name='Users', body=json.dumps(seller_message_details, default=str))
        startPublish(exchange_name='', routing_key='user-buyer', service_name='Users', body=json.dumps(buyer_message_details))
        sendNotification(order.to_mongo().to_dict(), user_to_id=order.sellerUsername, message='Approved Your order Delivery')
        return order
    except Exception as err:
        logger.error(f"Error in approvedOrder() Method: {str(err)}")


def sellerDeliverOrder(order_id: str, deliverd: bool, delivered_work: dict):
    try:
        order_new = Order.objects.get(orderId=order_id).modify(set__delivered=deliverd, set__status="Deliverd", set__events__orderDelivered=datetime.datetime.now(), push__deliveredWork=delivered_work)
        order = Order.objects.get(orderId=order_id)
        logger.info(f"sellerDeliverdOrder() Method, Order with id {order_id} Found Successfully.")
        if order is not None:
            message_details = {
                'orderId': order_id,
                'buyerUsername': order.buyerUsername,
                'sellerUsername': order.sellerUsername,
                'title': order.offer.gigTitle,
                'description': order.offer.description,
                'orderUrl': '',
                'template': ''
            }
            startPublish(exchange_name='', routing_key='order-email', service_name='Notification', body=json.dumps(message_details))
            sendNotification(data=order.to_mongo().to_dict(), user_to_id=order.buyerUsername, message='Delivered your order')
            return order
    except Exception as err:
        logger.error(f"Error in sellerDeliverOrder() Method : {str(err)}")


def requestDeliveryExtension(order_id: str, data: dict):
    try:
        order_new = Order.objects.get(orderId=order_id).modify(set__requestExtension__originalDate=data['originalDate'],
                                                      set__requestExtension__newDate=data['newDate'],
                                                      set__requestExtension__days=data['days'],
                                                      set__requestExtension__reason=data['reason'])
        print(f"Order is {order_new} and type is {type(order_new)}")
        order = Order.objects.get(orderId=order_id)
        logger.info(f"requestDeliveryExtension() Method , Delivery Extension for order with id {order_id} updated successfully.")
        message_details = {
            'buyer_username': order.buyerUsername,
            'seller_username': order.sellerUsername,
            'original_date': order.offer.oldDeliveryDate,
            'new_date': order.offer.newDeliveryDate,
            'reason': order.offer.reason,
            'orderUrl': '',
            'template': ''
        }
        startPublish(exchange_name='', routing_key='order-email', service_name='Notification', body=json.dumps(message_details, default=str))
        sendNotification(data=order.to_mongo().to_dict(), user_to_id=order.buyerUsername, message='request for an order delivery extension')
        return order
    except Exception as err :
        logger.error(f"Error in requestDeliveryExtension() Method: {str(err)}")


def approveDeliveryDate(order_id: str, data: dict):
    try:
        order_new = Order.objects.get(orderId=order_id).modify(set__offer__deliveryInDays=data['deliveryInDays'],
                                                      set__offer__newDeliveryDate=data['newDeliveryDate'],
                                                      set__offer__reason=data['reason'],
                                                      set__events__deliveryDateUpdate=data['newDeliveryDate'],
                                                      set__requestExtension__originalDate='',
                                                      set__requestExtension__newDate='',
                                                      set__requestExtension__days=0,
                                                      set__requestExtension__reason='')
        order = Order.objects.get(orderId=order_id)
        logger.info(f"approveDeliveryDate() Method , date extension for order with id {order_id} approved successfully.")
        message_details = {
            'subject': 'Congratulations, your extension request was approved.',
            'buyer_username': order.buyerUsername,
            'seller_username': order.sellerUsername,
            'header': 'Request Accepted',
            'type': 'accepted',
            'message': 'you can continue workin on the order',
            'orderUrl':'',
            'template': ''
        }
        startPublish(exchange_name='', routing_key='order-email', service_name='Notification', body=json.dumps(message_details))
        sendNotification(data=order.to_mongo().to_dict(), user_to_id=order.sellerUsername, message='approved your order delivery date extension')
        return order
    except Exception as err :
        logger.error(f"Error in approveDeliveryExtension() Method: {str(err)}")


def rejectDeliveryDate(order_id: str):
    try:
        order = Order.objects.get(id=order_id).modify(set__requestExtension__originalDate='',
                                                      set__requestExtension__newDate='',
                                                      set__requestExtension__days=0,
                                                      set__requestExtension__reason='')
        order.reload()
        logger.info(f"rejectDeliveryDate() Method, date extension for order with id {order_id} rejected.")
        message_details = {
            'subject': 'Sorry: your extension request was rejected',
            'buyer_username': order.buyerUsername,
            'seller_username': order.sellerUsername,
            'header': 'Request Rejected',
            'type': 'rejected',
            'message': 'you can contact the buyer for more information',
            'orderUrl': '',
            'template': ''
        }
        startPublish(exchange_name='', routing_key='order-email', service_name='NOtification', body=json.dumps(message_details))
        sendNotification(data=order.to_mongo().to_dict(), user_to_id=order.sellerUsername, message='rejected your order delivery date extension')
        return order
    except Exception as err:
        logger.error(f"Error in rejectDeliveryDate() Method : {str(err)}")
        

def updateOrderReview(data: dict):
    try:
        order = Order.objects.get(id=data['orderId']).modify(set__buyerReview__rating=data['rating'],
                                                             set__buyerReview__review=data['review'],
                                                             set__buyerReview__created=datetime.datetime.date(data['createdAt']),
                                                             set_sellerReview__rating=data['rating'],
                                                             set__sellerReview__review=data['review'],
                                                             set__sellerReview__created=datetime.datetime.date(data['createdAt']))
        order.reload()
        logger.info(f"updateOrderReview() Method, Review for order with id {data['orderId']} Updated successfully.")
        if data['type'] == 'buyer-review':
            sendNotification(data=order.to_dic(), user_to_id=order.sellerUsername, message=f"left you {data['rating']} start review")
        elif data['type'] == 'seller-review':
            sendNotification(data=order.to_mongo().to_dict(), user_to_id=order.buyerUsername, message=f"left you {data['rating']} start review")
        return order
    except Exception as err:
        logger.error(f"Error in updateOrderReview() Method : {str(err)}")
                     
        


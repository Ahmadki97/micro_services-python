from Helper_Users.logHandler import logger
from Models_Users.buyer_schema import Buyer
from Services.buyer_services import updateBuyerPurchasedGigs
from Services.seller_service import updateOngoingJobs, updateSellerCompletedJobs, updateTotalGigsCount, updateSellerCanceledJobs, updateSellerReview
from dotenv import load_dotenv
from Queus_Users.publish import startPublishGigs
import json
import os 
import pika, pika.exceptions
from datetime import datetime 

load_dotenv('.env')
def consumeBuyerMessage(channel, method, properties, body):
    try:
        data = json.loads(body)
        created_at = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S')
        print('Recieved Message is :', data)
        if data['type'] == 'auth':
            buyer = Buyer(
                username=data['username'],
                email=data['email'],
                profile_pic=data['profile_pic'],
                country=data['country'],
                created_at=created_at
            )
            buyer.save()
            logger.info(f"consumeBuyerMessage() Method: User {buyer.username} is added to Buyers..")
        else:
            buyer_id = data['buyer_id']
            purchased_gigs  = data['purchased_gigs']
            updateBuyerPurchasedGigs(buyer_id, purchased_gigs)
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as err:
        logger.error(f"Error in consumeBuyerMessage() Method : {str(err)} ")


def consumeSellerMessage(channel, method, properties, body):
    try:
        type = body['type']
        if type == 'create-order':
            updateOngoingJobs(seller_id=body['seller_id'], ongoing_jobs=body['ongoing_jobs'])
        elif type == 'approve-order':
            seller_data ={
                'seller_id': body['seller_id'],
                'ongoing_jobs': body['ongoing_jobs'],
                'completed_jobs': body['completed_jobs'],
                'total_earnings': body['total_earnings'],
                'recent_delievery': body['recent_delievery'],
            }
            updateSellerCompletedJobs(seller_data)
        elif type == 'update-gig-count':
            updateTotalGigsCount(seller_id=body['seller_id'], count=body['count'])
        elif type == 'cancel-order':
            updateSellerCanceledJobs(selelr_id=body['seller_id'])
        channel.basic_ack(delivery_tag=method.delivery_tag)

            
    except Exception as err:
        logger.error(f"Error in consumeSellerMessage() Method : {str(err)} ")


def consumeReviewMessage(channel, method, properties, body):
    try:
        type = body['type']
        if type == 'buyer-review':
            updateSellerReview(str(body))
            startPublishGigs(exchange_name='', routing_key='update-gig', body=json.dumps(body))
            # When Review Service is done i should check the data that being sent to the review Service (body)
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as err:
        logger.error(f"Error in consumeReviewMessage() Method : {str(err)}")
 


def startConsumeBuyerMessage():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL')))
            channel = connection.channel()
            channel.queue_declare(queue='user-buyer', durable=True)
            channel.basic_consume(queue='user-buyer', on_message_callback=consumeBuyerMessage)
            logger.info('Consumer For user-Buyer Started and waiting for New Messages')
            channel.start_consuming()
        except pika.exceptions as err:
            logger.error(f"Error in startConsumeBuyerMessage() Method: {str(err)}")  
             

def startconsumeSellerMessage():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL')))
            channel = connection.channel()
            channel.queue_declare(queue='order-seller', durable=True)
            channel.basic_consume(queue='order-seller', on_message_callback=consumeSellerMessage)
            logger.info('Consumer For User-Seller Started and waiting for New Messages')
            channel.start_consuming()
        except pika.exceptions as err:
            logger.error(f"Error in startConsumeSellerMessage() Method: {str(err)}")  
    

def startConsumeReviewFanoutMessage():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL')))
            channel = connection.channel()
            channel.exchange_declare(exchange='review-user-exchange', exchange_type='fanout')
            channel.queue_declare(queue='review-user', durable=True)
            channel.queue_bind(queue='review-user', exchange='review-user-exchange', routing_key='')
            channel.basic_consume(queue='seller-order', on_message_callback=consumeSellerMessage)
            logger.info('Consumer For Review-User Started and waiting for New Messages')
            channel.start_consuming()
        except pika.exceptions as err:
            logger.error(f"Error in startConsumeReviewFanoutMessage() Method: {str(err)}")  
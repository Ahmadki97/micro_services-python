from Helper_Order.logHandler import logger
from Services_Order.order_service import updateOrderReview
import pika
import os 



def startConsumeReviewFanoutMessage():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL')))
            channel = connection.channel()
            channel.exchange_declare(exchange='review-user-exchange', exchange_type='fanout')
            channel.queue_declare(queue='order-review', durable=True)
            channel.queue_bind(queue='order-review', exchange='review-user-exchange', routing_key='')
            channel.basic_consume(queue='seller-order', on_message_callback=updateOrderReview, auto_ack=True)
            logger.info('Consumer For Review-User Started and waiting for New Messages')
            channel.start_consuming()
        except Exception as err:
            logger.error(f"Error in startConsumeReviewFanoutMessage() Method: {str(err)}")  
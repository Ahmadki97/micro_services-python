import pika, pika.exceptions 
import json
from parameters import rabbitmq_host, rabbitmq_queue
from emails import activationMail
from logHandler import logger
import logging


async def callback(ch, method, properties, body):
    user_data = json.loads(body)
    logger.info('Received Message Body is :', user_data)
    print('Received Message:', user_data)

    activationMail(user_data)

def startConsumeAuthMail():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
            channel = connection.channel()
            channel.queue_declare('register', durable=True)
            channel.basic_consume(queue=rabbitmq_queue, on_message_callback=callback, auto_ack=True)
            logger.info('Consumer For AuthMail Started and waiting for New Messages')
            channel.start_consuming()   
        except pika.exceptions.AMQPConnectionError as e: 
            logger.error('Connection lost. Attempting to reconnect...')
            logger.warning(str(e))
            logging.error('Connection lost. Attempting to reconnect...')
            logging.warning('The error is : ', str(e))
            continue
        except KeyboardInterrupt:
            print('Consumer stopped (Keyboard Interrupt).')
            break

def startConsumeOrderMail():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
            channel = connection.channel()
            channel.queue_declare('order', durable=True)
            channel.basic_consume(queue="order", on_message_callback=callback, auto_ack=True)
            logger.info('Consumer For OrderMail Started and waiting for New Messages')
            channel.start_consuming()   
        except pika.exceptions.AMQPConnectionError as e: 
            logger.error('Connection lost. Attempting to reconnect...')
            logger.warning(str(e))
            logging.error('Connection lost. Attempting to reconnect...')
            logging.warning('The error is : ', str(e))
            continue
        except KeyboardInterrupt:
            print('Consumer stopped (Keyboard Interrupt).')
            break

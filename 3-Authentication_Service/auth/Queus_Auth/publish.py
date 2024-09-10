import pika
import os 
import logging
import json
from Helper_Auth.logHandler import logger
from dotenv import load_dotenv

load_dotenv('.env')


def startPublishAuth(queue, exchange_name, routing_key, body):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_URL')))
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=body)
        logger.info('Publisher For AuthMail Started and Publishing New Message')
    except Exception as e: 
        logger.error(f"Connection lost startPublishAuth(). Attempting to reconnect...{str(e)}")
        logger.warning(str(e))
        logging.error('Connection lost startPublishAuth(). Attempting to reconnect...')
        logging.warning(f"The error is : {str(e)}")
    except KeyboardInterrupt:
        print('Consumer stopped (Keyboard Interrupt).')

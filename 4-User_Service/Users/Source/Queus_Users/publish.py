import pika
import os 
import logging
import json
from Helper_Users.logHandler import logger
from dotenv import load_dotenv

load_dotenv('.env')


def startPublishGigs(exchange_name, routing_key, body):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_URL')))
        channel = connection.channel()
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json.loads(body))
        logger.info('Publisher For Gigs Started and Publishing New Message')
    except Exception as e: 
        logger.error(f"Connection lost startPublishGigs(). Attempting to reconnect...{str(e)}")
        logger.warning(str(e))
        logging.error('Connection lost startPublishGigs(). Attempting to reconnect...')
        logging.warning(f"The error is : {str(e)}")
    except KeyboardInterrupt:
        print('Consumer stopped (Keyboard Interrupt).')

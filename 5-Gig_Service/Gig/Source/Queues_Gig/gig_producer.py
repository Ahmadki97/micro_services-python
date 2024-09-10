import pika
import os 
import logging
import json
from pika.exceptions import AMQPConnectionError
import pika.exceptions
from Helper_Gig.logHandler import logger
from dotenv import load_dotenv

load_dotenv('.env')


def startPublishGigs(exchange_name, routing_key, body):
    try:
        print('RabbitMQ Host is :', os.getenv('RABBITMQ_URL'))
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_URL')))
        channel = connection.channel()
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json.dumps(body))
        logger.info('Publisher For Gigs Started and Publishing New Message')
    except Exception as err: 
        logger.error(f"Connection lost startPublishGigs(). Attempting to reconnect...{str(err)}")
    except KeyboardInterrupt:
        print('Consumer stopped (Keyboard Interrupt).')

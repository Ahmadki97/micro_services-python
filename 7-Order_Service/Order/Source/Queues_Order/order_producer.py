import pika.exceptions
from Helper_Order.logHandler import logger
from dotenv import load_dotenv
import pika
import json
import os


load_dotenv('.env')


def startPublish(exchange_name, routing_key, body, service_name):
    try:
        print('RabbitMQ Host is :', os.getenv('RABBITMQ_URL'))
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_URL')))
        channel = connection.channel()
        channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=json.dumps(body))
        logger.info(f"Puplishing New Message for the {service_name}")
    except Exception as err: 
        logger.error(f"Connection lost startPublish(). Attempting to reconnect...{str(err)}")

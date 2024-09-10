from dotenv import load_dotenv
from Helper_Order.logHandler import logger
import pika
import os 

load_dotenv('.env')

def checkRabbitConnection():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_URL')))
        logger.info(f"Service is Connected to RabbitMQ checkRabbitConnection() {connection}")
        connection.close()
    except Exception as err:
        str_err = str(err)
        logger.error(f"Error connecting to RabbitMQ checkRabbitConnection() {str_err}")
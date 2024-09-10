import pika 
import dotenv
from dotenv import load_dotenv
from Helper_Gig.logHandler import logger
import os 

load_dotenv('.env')

def checkRabbitConnection():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_URL')))
        logger.info(f"Service is Connected to RabbitMQ checkRabbitConnection() {connection}")
        connection.close()
    except pika.exceptions.AMQPConnectionError as err:
        str_err = str(err)
        logger.error(f"Error connecting to RabbitMQ checkRabbitConnection() {str_err}")
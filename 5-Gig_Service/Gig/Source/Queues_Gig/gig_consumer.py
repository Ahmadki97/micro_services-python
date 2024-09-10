from Helper_Gig.logHandler import logger
from dotenv import load_dotenv
from Queues_Gig.gig_producer import startPublishGigs
from Services_GIg.gig_service import updateGigReview, seedData
import json
import os 
import pika, pika.exceptions

load_dotenv('.env')
def consumeGigDirectMessage(channel, method, properties, body):
    try:
        data = json.loads(body)
        print('Recieved Message is :', data)
        updateGigReview(data)
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as err:
        logger.error(f"Error in consumeBuyerMessage() Method : {str(err)} ")    

def consumeSeedDirectMessage(channel, method, properties, body):
  try:
    data = json.loads(body)
    print(f"Data type is {type(data)}")
    if data['type'] == 'sellers_seeded':
        sellers = data['sellers']
        count = data['count']
        print(f"Type of sellers is {type(sellers)}")
        seedData(sellers, count)
        channel.basic_ack(delivery_tag=method.delivery_tag)
  except Exception as err:
      logger.error(f"Error in consumeSeedDirectMessage() Method {str(err)}")
            
    


def startConsumeGigDirectMessage():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL')))
        channel = connection.channel()
        channel.queue_declare(queue='update-gig', durable=True)
        channel.basic_consume(queue='update-gig', on_message_callback=consumeGigDirectMessage)
        logger.info('Consumer For user-gig Started and waiting for New Messages')
        channel.start_consuming()
    except pika.exceptions as err:
        logger.error(f"error in stratConsumeGigDirectMessage() Method : {str(err)}")


def startconsumeSeedDirectrMessage():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBITMQ_URL')))
        channel = connection.channel()
        channel.queue_declare(queue='recieve-sellers', durable=True)
        channel.basic_consume(queue='recieve-sellers', on_message_callback=consumeSeedDirectMessage)
        logger.info('Consumer For recieve-sellers Started and waiting for New Messages')
        channel.start_consuming()
    except pika.exceptions as err:
        logger.error(f"error in stratConsumeGigDirectMessage() Method : {str(err)}")


def startConsumeReviewFanoutMessage():
    pass 
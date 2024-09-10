import time
from logHandler import logger
import logging

def checkConnection(client):
    is_connected = False
    while not is_connected:
        try:
            if client.ping():
                print("PING Status", client.ping())
                is_connected = True
                response = client.cluster.health()
                if response['status'] == 'green':
                    logger.info(f"Notification Service Elastic Health Status: {response}")
                if response['status'] == 'yellow':
                    logger.info(f"Notification Service Elastic Health Status: {response}")
                if response['status'] == 'red':
                    logger.info(f"Notification Service Elastic Health Status: {response}")
                logger.info("Connected to Elasticsearch server")
        except ConnectionError as error:
            logger.error("Error connecting to Elasticsearch server",error)
            logging.error("Error connecting to Elasticsearch server",error)
            time.sleep(2)





            
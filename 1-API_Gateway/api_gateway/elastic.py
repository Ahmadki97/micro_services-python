from logHandler import logger
from elasticsearch import Elasticsearch
import os 
import logging


class ElasticSearch():
    client = Elasticsearch(os.getenv('ELASTIC_SEARCH_URL'))


    def checkConnection(self):
        print("Checking Elasticsearch Connection")
        is_connected = False
        while not is_connected:
            try:
                logger.info("Gateway Server is connected to ElasticSearch")
                logger.info(f"ElasticSearch Status is {self.client.cluster.health()}")
                is_connected = True
            except Exception as err:
                logging.info("Connection to ElasticSearch failed, Retrying...")
                logging.error(f"Gateway Service checkConnection() Function error: {str(err)}")



elastic_connection = ElasticSearch()
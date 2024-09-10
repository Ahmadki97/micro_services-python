from Helper_Users.logHandler import logger
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
                logger.info("Users Server is connected to ElasticSearch")
                logger.info(f"ElasticSearch Status is {self.client.cluster.health()}")
                is_connected = True
            except Exception as err:
                logging.info("Connection to ElasticSearch failed, Retrying...")
                logging.error(f"Users Service checkConnection() Function error: {str(err)}")


    def checkIfindexExists(self, index_name):
        result = self.client.indices.exists(index=index_name)
        return result
    

    def createIndex(self, index_name):
        try:
            result = self.checkIfindexExists(index_name)
            if result is True:
                logging.info(f"Index {index_name} already exists")
            else:
                self.client.indices.create(index=index_name)
                self.client.indices.refresh(index=index_name)
                logging.info(f"index {index_name} is created successfully.")
        except Exception as err:
            logging.error(f"Error has Occured while creating the index: {index_name}")


    def getDocumentById(self, index_name, document_id):
        try:
            result = self.client.get(index=index_name, id=document_id)
            return result._source
        except Exception as err:
            logging.error(f"Error in AuthService elasticsearch getDocumentById() Method {str(err)}")



elastic_connection = ElasticSearch()
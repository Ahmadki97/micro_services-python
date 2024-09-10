from Helper_Gig.logHandler import logger
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
                logger.info("Gig Server is connected to ElasticSearch")
                logger.info(f"ElasticSearch Status is {self.client.cluster.health()}")
                is_connected = True
            except Exception as err:
                logging.info("Connection to ElasticSearch failed, Retrying...")
                logging.error(f"Gig Service checkConnection() Function error: {str(err)}")


    def checkIfindexExists(self, index_name):
        result = self.client.indices.exists(index=index_name)
        return result
    

    def getDocumentCount(self, index):
        try:
            result = self.client.count(index=index)
            print('Count is :', result['count'])
            return result['count']
        except Exception as err:
            logger.error(f"Error in getDocumentCount() Method: {str(err)}")
    

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
            return result['_source']
        except Exception as err:
            logging.error(f"Error in GigService elasticsearch getDocumentById() Method {str(err)}")


    def addDocument(self, index_name: str, document_id: str, document):
        try:
            result = self.client.index(index=index_name, id=document_id, document=document)
            logger.info(f"Document With id {document_id} added successfully.")
            return result
        except Exception as err:
            logger.error(f"Error in elasticsearch updateDocument() Method {str(err)}")
            return []
        

    def updateDocument(self, index_name, document_id, document):
        try:
            result = self.client.update(index=index_name, id =document_id, doc=document)
            logger.info(f"Document with id {document_id} updated successfully.")
            return result
        except Exception as err:
            logger.error(f"Error in elasticsearch updateDocument() Method {str(err)}")
            return []
        
        

    def deleteDocument(self, index_name: str, document_id: str):
        try:
            result = self.client.delete(index=index_name, id=document_id)
            logger.info(f"Document with id {document_id} deleted successfully.")
            return result
        except Exception as err:
            logger.error(f"Error in elasticsearch deleteDocument() Method {str(err)}")
            return []



elastic_connection = ElasticSearch()
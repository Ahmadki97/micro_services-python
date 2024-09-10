import logging
from elasticsearch import Elasticsearch
import json
import datetime
import os 
from dotenv import load_dotenv

load_dotenv('.env')
# Assuming 'client' is an Elasticsearch client instance

print(f"Elastic URL is {os.getenv('ELASTIC_SEARCH_URL')}")
client = Elasticsearch(os.getenv('ELASTIC_SEARCH_URL'))

class ElasticsearchHandler(logging.Handler):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.json_documents = []

    def emit(self, record):
        document = {
            'message': record.msg,
            'levelname': record.levelname,
            'timestamp': datetime.datetime.utcnow().isoformat(),       
            }
        json_document = json.dumps(document)
        self.client.index(index='api_gateway_service', document=json_document)




# Create an instance of the handler
handler = ElasticsearchHandler(client)

# Set the formatter for the handler
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger = logging.getLogger('api_gateway')
logger.handlers.clear()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
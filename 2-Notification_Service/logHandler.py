import logging
from elasticsearch import Elasticsearch
from parameters import elasticsearch_url
import json
import datetime
import time
# Assuming 'client' is an Elasticsearch client instance
client = Elasticsearch(elasticsearch_url)

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
        self.client.index(index='notification_service', document=json_document)
        time.sleep(2)




# Create an instance of the handler
handler = ElasticsearchHandler(client)

# Set the formatter for the handler
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger = logging.getLogger('notification')
logger.handlers.clear()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
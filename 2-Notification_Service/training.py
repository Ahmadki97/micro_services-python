from parameters import elasticsearch_url
from elasticsearch import Elasticsearch

client = Elasticsearch(elasticsearch_url)

response = client.cluster.health()

print(response)
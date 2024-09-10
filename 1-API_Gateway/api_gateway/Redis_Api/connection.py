from redis import Redis
from Helper_api.elastic import logger
from dotenv import load_dotenv
import os 


load_dotenv('.env')
print('Redis URL is:', os.getenv('REDIS_HOST'))
client = Redis.from_url(os.getenv('REDIS_HOST'))

class RedisConnection():


    def __init__(self):
        self.client = client

    def redisConnect(self):
        try:
            logger.info(f"GateWay Service Redis Connection Status : {self.client.ping}")
        except Exception as err:
            logger.error(f"Error in redisConnect() Method : {str(err)}")



redis_connection = RedisConnection()

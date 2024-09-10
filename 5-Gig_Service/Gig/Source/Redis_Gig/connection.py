from redis import Redis
from Helper_Gig.logHandler import logger
from dotenv import load_dotenv
import os 


load_dotenv('.env')
redis_client = Redis.from_url(os.getenv('REDIS_HOST'))

def redisConnect():
    try:
        logger.info(f"Gig Service Redis Connection Status : {redis_client.ping}")
    except Exception as err:
        logger.error(f"Error in redisConnect() Method : {str(err)}")

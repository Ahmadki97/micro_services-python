from Helper_Gig.logHandler import logger 
from Redis_Gig.connection import redis_client



def getUserSelectedGigCategory(key: str):
    try:
        if redis_client.ping:
            response = redis_client.get(key)
            print('Response is ', response)
            return response
    except Exception as err:
        logger.error(f"Error in getUserSelectedGigCategory() Method : {str(err)}")
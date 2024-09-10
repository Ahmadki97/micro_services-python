from Helper_api.elastic import logger
from Redis_Api.connection import redis_connection


class GateWayCach():

    def __init__(self):
        self.client = redis_connection.client

    
    def saveUserSelectedCategory(self, key: str, value: str):
        try:
            self.client.set(name=key, value=value)
        except Exception as err:
            logger.error(f"Error in saveUserSelectedCategory() Method : {str(err)} ")
    


    def saveLoggedInUserToCash(self, key: str, value: str):
        try:
            index = self.client.lpos(name=key, value=value)
            if index is None:
                self.client.lpush(name=key, value=value)
                logger.info(f"saveLoggedInUserToCash() Method: User {value} is added.")
                response = self.client.lrange(name=key, start=0, end=-1)
                return response
        except Exception as err:
            logger.error(f"Error in saveLoggedInUserToCash() Method : {str(err)} ")
            return []
        


    def getLoggedInUsersFromCash(self, key: str):
        try:
            response = self.client.lrange(name=key, start=0, end=-1)
            return response
        except Exception as err:
            logger.error(f"Error in getLoggedInUserFromCash() Method : {str(err)} ")
            return []
    


    def removeLoggedOutUserFromCash(self, key: str, value: str):
        try:
            self.client.lrem(count=1, name=key, value=value)
            logger.info(f"removeLoggedOutUserFromCash() Method : User {value} Removed Successfully.")
            response = self.client.lrange(name=key, start=0, end=-1)
            return response
        except Exception as err:
            logger.error(f"Error in removeLoggedOutUserFromCash() Method : {str(err)} ")
            return []
    
import pymongo
import os 
from Helper_Chat.logHandler import logger
from dotenv import load_dotenv

load_dotenv('/usr/src/app/.env')

def dataBaseConnection():
    try:    
        client = pymongo.MongoClient(f"mongodb://{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}")
        logger.info(f"Chat Service Successfully Connected to DataBase.. DataBase Server Status is {str(client.server_info())}")
    except Exception as err:
        logger.error(f"Chat Service DataBaseConnection Method Error: {str(err)}")
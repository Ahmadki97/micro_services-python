from flask_jwt_extended import JWTManager, decode_token
from flask_cors import CORS
from flask_compress import Compress
from Helper_Users.elastic import elastic_connection
from Queus_Users.connection import checkRabbitConnection
from Queus_Users.user_consumer import startConsumeBuyerMessage, startconsumeSellerMessage
from Users_Controllers.Buyer.get import buyer_blue_print
from Users_Controllers.Seller.seed import seller_seed_blueprint
from Users_Controllers.Seller.create import create_seller_blueprint
from Users_Controllers.Seller.update import update_seller_blueprint
from Users_Controllers.Seller.get import get_seller_blueprint
from dotenv import load_dotenv
from datetime import timedelta
from Helper_Users.logHandler import logger
from mongoengine import connect
from database import dataBaseConnection
from app import app
import os 
import threading



connect(db='micro_users', host='mongo', port=27017, username='root', password='root')
load_dotenv('.env')


class Server():
    
    def __init__(self):
        self.app = app
        self.jwt = JWTManager(self.app)
        self.cors = CORS(self.app)
        self.compress = Compress()
        


    def start(self):
        print(__name__)
        elastic_connection_thred = threading.Thread(target=self.startElasticSearch)
        self.securityMiddleware()
        self.standardMiddleware()
        self.routesMiddleware()
        self.dbConnection()
        elastic_connection_thred.start()
        self.startQueues()
        self.app.run(host='0.0.0.0', port=os.getenv('PORT'), debug=True)  
        
    

    def securityMiddleware(self):
        try:
            self.app.config['JWT_SECRET_KEY'] = os.getenv('JWT_TOKEN')
            self.app.config['JWT_TOKEN_LOCATION'] = ['cookies']
            self.app.config['JWT_COOKIE_SECURE'] = False
            self.app.config['SESSION_COOKIE_NAME'] = 'session'
            self.app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
            logger.info('Security Middleware() has been initialized.')
        except Exception as err:
            str_err = str(err)
            logger.error(f"Error in Security MiddleWare() Function: {str_err}")


    def standardMiddleware(self):
        try:
            self.compress.init_app(self.app)
            logger.info("Standard Middleware() has been initialized")
        except Exception as err:
            str_err = str(err)
            logger.error(f"Error in Standard Middleware() Function : {str_err}")

    
    def routesMiddleware(self):
            try:
                self.app.register_blueprint(buyer_blue_print)
                self.app.register_blueprint(update_seller_blueprint)
                self.app.register_blueprint(get_seller_blueprint)
                self.app.register_blueprint(create_seller_blueprint)
                self.app.register_blueprint(seller_seed_blueprint)
                logger.info(f"routesMiddleware has been initialized..")
            except Exception as err:
                logger.error(f"Error in routesMiddleware() {str(err)}")
                


    def startElasticSearch(self):
        elastic_connection.checkConnection()


    def startQueues(self):
        seller_queue = threading.Thread(target=startconsumeSellerMessage)
        buyer_queue = threading.Thread(target=startConsumeBuyerMessage)
        connection_thread = threading.Thread(target=checkRabbitConnection)
        connection_thread.start()
        seller_queue.start()
        buyer_queue.start()
    
    def dbConnection(self):
        dataBaseConnection()


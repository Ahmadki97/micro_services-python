from flask_jwt_extended import JWTManager, decode_token
from flask_cors import CORS
from flask_compress import Compress
from Helper_Gig.logHandler import logger
from Helper_Gig.elastic import elastic_connection
from Queues_Gig.connection import checkRabbitConnection
from Redis_Gig.connection import redisConnect
from Queues_Gig.gig_consumer import startConsumeGigDirectMessage, startconsumeSeedDirectrMessage
from Controllers_Gig.create import creategig_blueprint
from Controllers_Gig.delete import deletegig_blueprint
from Controllers_Gig.get import getgig_blueprint
from Controllers_Gig.health import health_route
from Controllers_Gig.search import gigsearch_blueprint
from Controllers_Gig.seed import seedgig_blueprint
from Controllers_Gig.update import updategig_blueprint
from database import dataBaseConnection
from dotenv import load_dotenv
from datetime import timedelta
from mongoengine import connect
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
        rabbitmq_thread = threading.Thread(target=self.startQueues)
        self.securityMiddleware()
        self.standardMiddleware()
        self.routesMiddleware()
        elastic_connection_thred.start()
        rabbitmq_thread.start()
        self.dbConnection()
        self.redisConnection()
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
                self.app.register_blueprint(getgig_blueprint)
                self.app.register_blueprint(creategig_blueprint)
                self.app.register_blueprint(deletegig_blueprint)
                self.app.register_blueprint(seedgig_blueprint)
                self.app.register_blueprint(updategig_blueprint)
                self.app.register_blueprint(gigsearch_blueprint)
                self.app.register_blueprint(health_route)
                logger.info(f"routesMiddleware has been initialized..")
            except Exception as err:
                logger.error(f"Error in routesMiddleware() {str(err)}")
                


    def startElasticSearch(self):
        elastic_connection.checkConnection()
        elastic_connection.createIndex('gigs')


    def startQueues(self):
        checkRabbitConnection()
        seed_thread = threading.Thread(target=startconsumeSeedDirectrMessage)
        gig_thread = threading.Thread(target=startConsumeGigDirectMessage) 
        seed_thread.start()
        gig_thread.start()
    
    def dbConnection(self):
        dataBaseConnection()


    def redisConnection(self):
        redisConnect()


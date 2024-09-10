from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_compress import Compress
from Helper_Chat.logHandler import logger
from Helper_Chat.elastic import elastic_connection
from Queues_Chat.connection import checkRabbitConnection
from database import dataBaseConnection
from dotenv import load_dotenv
from Sockets_Chat.sockets_io import sio
from Controllers_Chat.create import create_blueprint
from Controllers_Chat.update import update_blueprint
from Controllers_Chat.get import get_blueprint
from Controllers_Chat.health import health_route
from datetime import timedelta
from mongoengine import connect  
from app import app
import socketio
import threading
import os 



connect(db='messages', host='mongo', port=27017, username='root', password='root')
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
        self.app.wsgi_app = socketio.WSGIApp(sio, self.app.wsgi_app)
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
                self.app.register_blueprint(update_blueprint)
                self.app.register_blueprint(create_blueprint)
                self.app.register_blueprint(get_blueprint)
                self.app.register_blueprint(health_route)
                logger.info(f"routesMiddleware has been initialized..")
            except Exception as err:
                logger.error(f"Error in routesMiddleware() {str(err)}")
                


    def startElasticSearch(self):
        elastic_connection.checkConnection()


    def startQueues(self):
        checkRabbitConnection()
        
    def dbConnection(self):
        dataBaseConnection()
    





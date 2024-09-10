from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_compress import Compress
from Helper_Review.logHandler import logger
from Helper_Review.elastic import elastic_connection
from sqlalchemy.exc import SQLAlchemyError
from Models_Review.database import db
from Queues_Review.connection import checkRabbitConnection
from Controller_Review.create import create_blueprint
from Controller_Review.get import get_blueprint
from Controller_Review.health import health_route
from dotenv import load_dotenv
from sqlalchemy import text
from datetime import timedelta  
from app import app
import threading
import os 
import logging


user = os.getenv('MYSQL_USER')
database = os.getenv('MYSQL_DATABASE')
host = os.getenv('MYSQL_HOST')
port = 5432
paswd = os.getenv('MYSQL_PASSWORD')


load_dotenv('.env')


class Server():
    
    
    def __init__(self):
        try:
            print(f"Hello from Server initization!")
            self.app = app
            self.app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{paswd}@{host}:{port}/{database}"
            self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            print(f"Database is {f"postgresql://{user}:{paswd}@{host}:{port}/{database}"}")
            db.init_app(self.app)
            with self.app.app_context():
                db.create_all()
            self.jwt = JWTManager(self.app)
            self.cors = CORS(self.app)
            self.compress = Compress()
        except Exception as err:
            logging.error(f"Error in initializing the server: {str(err)}")
                    


    def start(self):
        print(__name__)
        elastic_connection_thred = threading.Thread(target=self.startElasticSearch)
        rabbitmq_thread = threading.Thread(target=self.startQueues)
        self.securityMiddleware()
        self.standardMiddleware()
        self.routesMiddleware()
        elastic_connection_thred.start()
        rabbitmq_thread.start()
        self.checkPostgresqlConnection()
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
                self.app.register_blueprint(create_blueprint)
                self.app.register_blueprint(get_blueprint)
                self.app.register_blueprint(health_route)
                logger.info(f"routesMiddleware has been initialized..")
                pass 
            except Exception as err:
                logger.error(f"Error in routesMiddleware() {str(err)}")
                


    def startElasticSearch(self):
        elastic_connection.checkConnection()


    def startQueues(self):
        checkRabbitConnection()


    def checkPostgresqlConnection(self):
        try:
            with self.app.app_context():    
                db.session.execute(text('?'))
                logger.info("Review Service is Connected to Postgres checkMysqlConnection() ")
        except SQLAlchemyError as err:
            str_err = str(err)
            logger.error(f"Error connecting to postgres Server checkDbConnection() : {str_err}")
    





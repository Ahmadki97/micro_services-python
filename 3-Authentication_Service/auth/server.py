from flask import Flask,request
from flask_login import LoginManager
from flask_jwt_extended import JWTManager, decode_token
from flask_cors import CORS
from flask_compress import Compress
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from Helper_Auth.logHandler import logger
from Queus_Auth.connection import checkRabbitConnection
from Controller_Auth.signup import signup_route
from Controller_Auth.verify_email import verify_email_route
from Controller_Auth.signin import signin_route
from Controller_Auth.change_password import change_password_routes
from Controller_Auth.current_user import current_user_routes
from Controller_Auth.search import search_route
from dotenv import load_dotenv
from Helper_Auth.elastic import elastic_connection
from datetime import timedelta
import os 
import threading



load_dotenv('.env')
login_manager = LoginManager()
app = Flask(__name__)
db = SQLAlchemy()
user = os.getenv('MYSQL_USER')
database = os.getenv('MYSQL_DATABASE')
host = os.getenv('MYSQL_HOST')
port = os.getenv('MYSQL_PORT')
paswd = os.getenv('MYSQL_PASSWORD')


class Server():
    
    def __init__(self):
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{user}:{paswd}@{host}:{port}/{database}"
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.db = db 
        login_manager.init_app(self.app)
        self.db.init_app(self.app)
        with self.app.app_context():
            self.db.create_all()
        self.jwt = JWTManager(self.app)
        self.cors = CORS(self.app)
        self.compress = Compress()
    

    def start(self):
        print(__name__)
        elastic_connection_thred = threading.Thread(target=self.startElasticSearch)
        queues_thread = threading.Thread(target=self.startQueues)
        self.securityMiddleware()
        self.standardMiddleware()
        self.routesMiddleware()
        elastic_connection_thred.start()
        queues_thread.start()
        self.checkMysqlConnection()  
        self.app.run(host='0.0.0.0', port='4001', debug=True)  
        
    

    def securityMiddleware(self):
        try:
            self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
            self.app.config['JWT_SECRET_KEY'] = os.getenv('JWT_TOKEN')
            self.app.config['JWT_TOKEN_LOCATION'] = ['cookies']
            self.app.config['JWT_COOKIE_SECURE'] = False
            self.app.config['SESSION_COOKIE_NAME'] = 'session'
            self.app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
            logger.info('Security Middleware() for Authentication Service has been initialized.')
            @self.app.before_request
            def before_request():
                token = request.headers.get('Authorization')
                if token:
                    token = token.split(' ')[1]
                    try:
                        payload = decode_token(token)
                        request.current_user = payload
                    except Exception as err:
                        logger.error(f"Erron in before_request() Method in SecurityMiddleware")
        except Exception as err:
            str_err = str(err)
            logger.error(f"Error in Security MiddleWare() Function: {str_err}")


    def standardMiddleware(self):
        try:
            self.compress.init_app(self.app)
            logger.info("Standard Middleware() for Authentication Service has been initialized")
        except Exception as err:
            str_err = str(err)
            logger.error(f"Error in Standard Middleware() Function : {str_err}")

    
    def routesMiddleware(self):
            try:
                self.app.register_blueprint(signin_route)
                self.app.register_blueprint(signup_route)
                self.app.register_blueprint(change_password_routes)
                self.app.register_blueprint(current_user_routes)
                self.app.register_blueprint(verify_email_route)
                self.app.register_blueprint(search_route)

                logger.info(f"routesMiddleware has been initialized..")
            except Exception as err:
                logger.error(f"Error in routesMiddleware() {str(err)}")
                


    def startElasticSearch(self):
        elastic_connection.checkConnection()


    def startQueues(self):
        checkRabbitConnection() 


    def checkMysqlConnection(self):
        try:
            with self.app.app_context():    
                db.session.execute(text('show tables;'))
                logger.info("Auth Service is Connected to MySQL checkMysqlConnection() ")
        except SQLAlchemyError as err:
            str_err = str(err)
            logger.error(f"Error connecting to MYSQL Server checkDbConnection() : {str_err}")

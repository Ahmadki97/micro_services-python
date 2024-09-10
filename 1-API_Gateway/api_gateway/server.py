from flask import Flask, request, jsonify
from flask_session import Session
from flask_restful import Resource, Api
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_compress import Compress
from redis import Redis, StrictRedis
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import timedelta
from logHandler import logger
from elastic import elastic_connection
from Routes_API.auth_service import auth_blue_print
from dotenv import load_dotenv
from Routes_API.buyer_service import buyer_blue_print
from Routes_API.seller_service import seller_blueprint
from Routes_API.gig_service import gig_blue_print
from Routes_API.chat_service import chat_blue_print
from Routes_API.order_service import order_blue_print
from Routes_API.review_service import review_blue_print
from Sockets_Api.socket import chat_io, order_io
import threading
import os




load_dotenv('.env')
app = Flask(__name__)
jwt = JWTManager(app)

class gateWayServer(Resource):


    def __init__(self):
        self.app = app
       # self.jwt = JWTManager(self.app)  
        self.api = Api(self.app)
        self.compress = Compress()
        self.securityMiddleware()
        self.standardMiddleware()
        self.routesMiddleware()

    def start(self):
        print("Server has started..")
        elastic_connection_thred = threading.Thread(target=self.startElasticSearch)
        elastic_connection_thred.start()
        self.createSocketIo()
        self.app.run(host='0.0.0.0', port=os.getenv('PORT'), debug=True)
        
        

    def securityMiddleware(self):
        try:
            ## Must Use Talisman and CSRFPROTECT     
            self.api.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
            self.api.app.config['JWT_SECRET_KEY'] = os.getenv('JWT_TOKEN')
            print(f"JWT Token is {os.getenv('JWT_TOKEN')}")
            self.api.app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
            self.api.app.wsgi_app = ProxyFix(self.app.wsgi_app) # To tell Flask app that its running behind a proxy
            self.api.app.config['JWT_TOKEN_LOCATION'] = ['cookies'] # To save jwt auth token into cookies 
            self.api.app.config['JWT_ACCESS_CSRF_HEADER_NAME'] = 'X-CSRF-TOKEN'
            self.api.app.config['JWT_ACCESS_CSRF_FIELD_NAME'] = 'csrf'
            self.api.app.config['JWT_COOKIE_SECURE'] = False # Only allow JWT cookies to be sent over https. In production, this should likely be True
            self.api.app.config['SESSION_COOKIE_NAME'] = 'session'
            self.api.app.config['JWT_COOKIE_CSRF_PROTECT'] = True 
            self.api.app.config['JWT_CSRF_METHODS'] = ['POST', 'PUT', 'PATCH', 'DELETE']  # Specify methods that require CSRF protection
            self.api.app.config['JWT_CSRF_CHECK_FORM'] = True  # Enable CSRF form check
            self.api.app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
            # self.app['SESSION_COOKIE_SECURE'] = { Should Be modified Later }  # Browsers will only send cookies with requests over HTTPS if the cookie is marked “secure”. The application must be served over HTTPS for this to make sense
            cors = CORS(self.api.app, origins='')
            # Allows users to make authenticated requests. If true, injects the Access-Control-Allow-Credentials header in responses. This allows cookies and credentials to be submitted across domains.
            logger.info("flask app security Middleware() is initialized")
        except Exception as error:
            str_error = str(error)
            logger.error(f"Error in securityMiddleware() Function {str_error}")

    def standardMiddleware(self):
        try:
            self.compress.init_app(self.api.app) # this is Used to compress Responses with gzips 
            # app.use(json({ limit: '200mb' })); // This Functionality is by default achieved in python flask using request.get_json()
            # if the request.content_type is 'application/json

            # app.use(urlencoded({ extended: true, limit: '200mb' })); // This Functionality is by default achueved in flask using request.form.to_dict()
            # if the request.content_type is application/x-www-form-urlencoded
            logger.info("flask app standardMiddleWare() is initialized")
        except Exception as error:
            str_error = str(error)
            logger.error(f"Error in standardMiddleware() Function : {str_error}")

    
    def startElasticSearch(self):
        print('Starting Connection TO elasticsearch')
        elastic_connection.checkConnection()

    def routesMiddleware(self):        
        self.app.register_blueprint(auth_blue_print)
        self.app.register_blueprint(seller_blueprint)
        self.app.register_blueprint(buyer_blue_print)
        self.app.register_blueprint(gig_blue_print)
        self.app.register_blueprint(chat_blue_print)
        self.app.register_blueprint(order_blue_print)
        self.app.register_blueprint(review_blue_print)


    def createSocketIo(self):
      print(f"Chat Service Url is : {os.getenv('MESSAGE_BASE_URL')}")
      chat_io.connect(url=os.getenv('MESSAGE_BASE_URL'))
      order_io.connect(url=os.getenv('ORDER_BASE_URL'))

    
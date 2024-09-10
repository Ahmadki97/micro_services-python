import base64
from flask import jsonify, Blueprint
from services.auth_middleware import custom_jwt_required
from Helper_api.requests import Requests
from Helper_api.elastic import logger
from Helper_api.errorhandlers import ServerError
from dotenv import load_dotenv
import os 
import json

load_dotenv('.env')
service_url = os.getenv('USERS_BASE_URL')
base_url = f"{service_url}/api/v1/users/sellers"
seller_client = Requests(service_url=base_url)
seller_blueprint = Blueprint('Seller_Routes', __name__, url_prefix='/api/v1/users/sellers')


@seller_blueprint.route('/getseller-id/<string:id>', methods=['GET'])
@custom_jwt_required
def getSellerById(id):
    try:
        response = seller_client.makeRequest(endpoint=f"getseller-id/{id}", service_token='sellers')
        return json.loads(response)
    except Exception as err:
        logger.error(f"Error in getSellerId() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getSellerById() Function")
    

@seller_blueprint.route('/getseller-username/<string:username>', methods=['GET'])
@custom_jwt_required
def getSellerByUsername(username):
    try:
        response = seller_client.makeRequest(endpoint=f"getseller-username/{username}", service_token='sellers')
        return json.loads(response)
    except Exception as err:
        logger.error(f"Error in getCurrentUser() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getSellerById() Function")


@seller_blueprint.route('/getseller-id/<int:count>', methods=['GET'])
@custom_jwt_required    
def getRandomSellers():
    try:
        seller_client.makeRequest(endpoint='/getseller-random/<int:count>', service_token='sellers')
        return(jsonify('Request is sent to the applicable Service'))
    except Exception as err:
        logger.error(f"Error in getCurrentUser() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getRandomSellers() Function")


@seller_blueprint.route('/create-seller', methods=['POST'])
@custom_jwt_required
def createSeller():
    try:
        response = seller_client.makeRequest(endpoint='create-seller', service_token='sellers')
        return json.dumps(response)
    except Exception as err:
        logger.error(f"Error in getCurrentUser() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "createSeller() Function")


@seller_blueprint.route('/updateseller-id/<string:id>', methods=['PUT'])
@custom_jwt_required
def updateSeller(id):
    try:
        response = seller_client.makeRequest(endpoint=f"updateseller-id/{id}", service_token='sellers')
        return json.loads(response)
    except Exception as err:
        logger.error(f"Error in getCurrentUser() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "updateSeller() Function")

@seller_blueprint.route('/seed-sellers/<int:count>', methods=['PUT'])
@custom_jwt_required
def seed(count):
    try:
        seller_client.makeRequest(endpoint=f"seed-sellers/{count}", service_token='sellers')
        return(jsonify('Request is sent to the applicable Service'))
    except Exception as err:
        logger.error(f"Error in getCurrentUser() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "updateSeller() Function")

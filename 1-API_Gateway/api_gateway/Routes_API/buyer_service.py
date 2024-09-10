from flask import jsonify, Blueprint
from services.auth_middleware import custom_jwt_required
from Helper_api.requests import Requests
from Helper_api.elastic import logger
from Helper_api.errorhandlers import ServerError
from dotenv import load_dotenv
import os 



load_dotenv('/usr/src/app/api_gateway/.env')
service_url = os.getenv('USERS_BASE_URL')
print(f"Service Url is : {service_url}")
base_url = f"{service_url}/api/v1/users/buyers"
buyer_client = Requests(service_url=base_url)
buyer_blue_print = Blueprint('buyer', __name__, url_prefix='/api/v1/users/buyers')


@buyer_blue_print.route('/username/<string:username>', methods=['GET'])
@custom_jwt_required
def getCurrentBuyerByUsername():
    try:
        buyer_client.makeRequest(endpoint='current-buyer', service_token='buyers')
        return(jsonify('Request is sent to the applicable Service'))
    except Exception as err:
        logger.error(f"Error in getCurrentUser() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getCurrentUser() Function")
    
@buyer_blue_print.route('/getbuyer-username', methods=['GET'])
@custom_jwt_required
def getBuyerByUsername():
    try:
        buyer_client.makeRequest(endpoint='getbuyer-username', service_token='buyers')
        return(jsonify('Request is sent to the applicaple Service'))
    except Exception as err:
        logger.error(f"Error in getBuyerByUsername() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getBuyerByUsername() Function")
    

@buyer_blue_print.route('getbuyer-email', methods=['GET'])
@custom_jwt_required
def getBuyerByEmail():
    try:
        buyer_client.makeRequest(endpoint='getbuyer-email', service_token='buyers')
        return(jsonify('Request is sent to the applicaple Service'))
    except Exception as err:
        logger.error(f"Error in getBuyerByEmail() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getBuyerByEmail() Function")
    
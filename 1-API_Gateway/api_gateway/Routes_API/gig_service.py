from flask import jsonify, Blueprint
from services.auth_middleware import custom_jwt_required
from Helper_api.requests import Requests
from Helper_api.elastic import logger
from Helper_api.errorhandlers import ServerError
from dotenv import load_dotenv
import os 



load_dotenv('/usr/src/app/api_gateway/.env')
service_url = os.getenv('GIG_BASE_URL')
print(f"Service Url is : {service_url}")
base_url = f"{service_url}/api/v1/gig"
gig_client = Requests(service_url=base_url)
gig_blue_print = Blueprint('Gig', __name__, url_prefix='/api/v1/gig')

@gig_blue_print.route('/getgig-id/<string:gig_id>', methods=['GET'])
@custom_jwt_required
def getGigById(gig_id: str):
    try:
        response = gig_client.makeRequest(endpoint=f"getgig-id/{gig_id}", service_token='gig')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in getGigById() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getGigById() Function")


@gig_blue_print.route('/getgig-seller/<string:seller_id>', methods=['GET'])
@custom_jwt_required
def getGigsSeller(seller_id: str):
    try:
        response = gig_client.makeRequest(endpoint=f"getgig-seller/{seller_id}", service_token='gig')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in getGigsSeller() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getGigsSeller() Function")


@gig_blue_print.route('/getgigspaused-seller/<string:seller_id>', methods=['GET'])
@custom_jwt_required
def getGigsPausedSeller(seller_id: str):
    try:
        response = gig_client.makeRequest(endpoint=f"getgigspaused-seller/{seller_id}", service_token='gig')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in getGigsPausedSeller() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getGigsPausedSeller() Function")



@gig_blue_print.route('/gettop-gig', methods=['GET'])
@custom_jwt_required
def getTopRatedGigsByCategory():
    try:
        response = gig_client.makeRequest(endpoint=f"gettop-gig", service_token='gig')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in getTopRatedGigsByCategory() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getTopRatedGigsByCategory() Function")



@gig_blue_print.route('/getgigs-category', methods=['GET'])
@custom_jwt_required
def getGigsByCategory():
    try:
        response = gig_client.makeRequest(endpoint=f"getgigs-category", service_token='gig')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in getGigsByCategory() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getGigsByCategory() Function")
    

@gig_blue_print.route('/getmore-gig/<string:gig_id>', methods=['GET'])
@custom_jwt_required
def getMoreLikeThis(gig_id: str):
    try:
        response = gig_client.makeRequest(endpoint=f"getmore-gig/{gig_id}", service_token='gig')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in getMoreLikeThis() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getMoreLikeThis() Function")
    

@gig_blue_print.route('/create-gig', methods=['POST'])
@custom_jwt_required
def createGig():
    try:
        response = gig_client.makeRequest(endpoint=f"create-gig", service_token='gig')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in createGig() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "createGig() Function")


@gig_blue_print.route('/delete-gig/<string:gig_id>/<string:seller_id>', methods=['DELETE'])
@custom_jwt_required
def deleteeGig(gig_id, seller_id):
    try:
        response = gig_client.makeRequest(endpoint=f"delete-gig/{gig_id}/{seller_id}", service_token='gig')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in deleteGig() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "deleteGig() Function")


@gig_blue_print.route('/gig-search', methods=['GET'])
@custom_jwt_required
def searchGig():
    try:
        response = gig_client.makeRequest(endpoint=f"gig-search", service_token='gig')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in searchGig() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "searchGig() Function")


@gig_blue_print.route('/seed-gig/<int:count>', methods=['POST'])
@custom_jwt_required
def seedGig(count: int):
    try:
        response = gig_client.makeRequest(endpoint=f"seed-gig/{count}", service_token='gig')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in seedGig() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "seedGig() Function")
    

@gig_blue_print.route('/update-gig/<string:gig_id>', methods=['PUT'])
@custom_jwt_required
def updateGig(gig_id: str):
    try:
        response = gig_client.makeRequest(endpoint=f"update-gig/{gig_id}", service_token='gig')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in updateGig() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "updateGig() Function")


@gig_blue_print.route('/updategig-active/<string:gig_id>', methods=['PUT'])
def updateGigActive(gig_id: str):
    try:
        response = gig_client.makeRequest(endpoint=f"updategig-active/{gig_id}", service_token='gig')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in updateGigActive() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "updateGigActive() Function")
    

@gig_blue_print.route('/api/v1/gig/health', methods=['GET'])
def health():
    try:
        response = gig_client.makeRequest(endpoint=f"health", service_token='gig')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in health() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "health() Function")    

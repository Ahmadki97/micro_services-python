from flask import request, jsonify, Blueprint
from Helper_api.requests import Requests
from Helper_api.elastic import logger
from Helper_api.errorhandlers import ServerError
from services.auth_middleware import custom_jwt_required
from dotenv import load_dotenv
import json
import os 


load_dotenv('.env')
service_url = os.getenv('REVIEW_BASE_URL')
print(f"Service Url is : {service_url}")
base_url = f"{service_url}/api/v1/review"
gig_client = Requests(service_url=base_url)
review_blue_print = Blueprint('Review', __name__, url_prefix='/api/v1/review')


@review_blue_print.route('/', methods=['POST'])
@custom_jwt_required
def createReview():
    try:
        response = gig_client.makeRequest(endpoint=f"", service_token='order')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in createReview() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "createOrder() Function")


@review_blue_print.route('/gig/<string:gig_id>', methods=['GET'])
@custom_jwt_required
def getReviewByGigId(gig_id: str):
    try:
        response = gig_client.makeRequest(endpoint=f"gig/{gig_id}", service_token='review')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in getReviewByGigId() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "createOrder() Function")


@review_blue_print.route('/seller/<string:seller_id>', methods=['GET'])
@custom_jwt_required
def getReviewBySellerrId(seller_id: str):
    try:
        response = gig_client.makeRequest(endpoint=f"seller/{seller_id}", service_token='review')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in getReviewBySellerrId Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "createOrder() Function")

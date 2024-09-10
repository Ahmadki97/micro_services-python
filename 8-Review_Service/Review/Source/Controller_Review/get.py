from Helper_Review.logHandler import logger
from Helper_Review.verify_token import jwt_required
from flask import request, Blueprint
from Services_Review.review_services import getReviewsByGigId, getReviewsBySellerId
from http import HTTPStatus
import json

get_blueprint = Blueprint('Get_Review_Blueprint', __name__, url_prefix='/api/v1/review')


@get_blueprint.route('/gig/<string:gig_id>', methods=['GET'])
@jwt_required
def reviewByGigId(gig_id: str):
    try:
        review = getReviewsByGigId(gig_id=gig_id)
        response = {
            "Message": f"reviews for gig with id {gig_id} found Successfully.",
            "Http Status": HTTPStatus.OK,
            "Review": review
        }
        return(json.dumps(response, default=str))
    except Exception as err:
        logger.error(f"Error in get review by gig id controller: {str(err)}")
        return(f"Could not get review, pleas try again later.")
    

@get_blueprint.route('/seller/<string:seller_id>', methods=['GET'])
@jwt_required
def reviewBySellerId(seller_id: str):
    try:
        review = getReviewsBySellerId(seller_id=seller_id)
        response = {
            "Message": f"reviews for seller with id {seller_id} found Successfully.",
            "Http Status": HTTPStatus.OK,
            "Review": review
        }
        return(json.dumps(response, default=str))
    except Exception as err:
        logger.error(f"Error in get review by gig id controller: {str(err)}")
        return(f"Could not get review, pleas try again later.")
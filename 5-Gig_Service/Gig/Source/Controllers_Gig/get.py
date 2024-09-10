from flask import request, Blueprint, jsonify
from Helper_Gig.logHandler import logger
from Helper_Gig.verify_token import jwt_required
from Services_GIg.gig_service import getGigId, getSellerGigs, getSellerPausedGigs
from Services_GIg.search_service import getTopRatedGIgByCategory,gigsSearchByCategory, getMoreGigsLikeThis 
from Redis_Gig.gig_cash import getUserSelectedGigCategory
from http import HTTPStatus
import json


getgig_blueprint = Blueprint('Get_Gig', __name__, url_prefix='/api/v1/gig')

@getgig_blueprint.route('getgig-id/<string:gig_id>', methods=['GET'])
@jwt_required
def gigById(gig_id):
    try:
        print('Gig_ID is :', gig_id)
        gig = getGigId(id=gig_id)
        logger.info(f"gigById() Method Gig {gig_id} found Successfully ")
        response = {
            'Message': 'Gig Found Successfully',
            'Gig': gig
        }
        return(response)
    except Exception as err:
        logger.error(f"Error in gigById() Method : {str(err)}")
        return(jsonify('Gig is not Found'))


@getgig_blueprint.route('/getgig-seller/<string:seller_id>', methods=['GET'])
@jwt_required
def getGigsSeller(seller_id: str):
    try:
        gigs = getSellerGigs(seller_id)
        logger.info(f"getGigsSeller() Method Gigs for Seller {seller_id} Found Successfully")
        response = {
            'Message': 'Gigs Found Successfully',
            'Gigs': gigs
        }
        return(response)
    except Exception as err:
        logger.error(f"error in getGigsSeller() Method : {str(err)}")
        return(jsonify('Gigs were Not Found'))
    

@getgig_blueprint.route('/getgigspaused-seller/<string:seller_id>', methods=['GET'])
@jwt_required
def getGigsPausedSeller(seller_id):
    try:
        gigs = getSellerPausedGigs(seller_id)
        logger.info(f"getGigsPausedSeller() Method Paused Gigs for Seller {seller_id} Found Successfully")
        response = {
            'Message': 'Gigs Found Successfully',
            'Gigs': gigs
        }
        return(json.loads(response)), HTTPStatus.OK
    except Exception as err:
        logger.error(f"Error in getGigsPausedSeller() Method : {str(err)}")
        return(jsonify("Gigs were not Found"))
    

# When user Selects a Category..Without Frontend this Controller Will not work
@getgig_blueprint.route('gettop-gig', methods=['GET'])
@jwt_required
def topRatedGigsByCategory():
    try:
        selected_category = getUserSelectedGigCategory(f"{request.get_json()['username']}")
        result_hits = []
        gigs = getTopRatedGIgByCategory(category_filter=selected_category)
        for gig in gigs:
            result_hits.append(gig)
            logger.info(f"topRatedGigsByCategory() Method: Top Rated Gigs Found for {selected_category}")
            response = {
                'Message': 'Top Rated Gigs Found',
                'gigs': result_hits,
            }
            return(jsonify(response)), HTTPStatus.OK
    except Exception as err:
        logger.error(f"Error in getTopRatedGigsByCategory() Method : {str(err)}")
        return jsonify('Top Rated Gigs were not found')
    
# Also Requires Cached Gigs in Redis
@getgig_blueprint.route('/getgigs-category', methods=['GET'])
@jwt_required
def gigsByCategory():
    try:
        selected_category = getUserSelectedGigCategory(f"{request.get_json()['username']}")
        result_hits = []
        gigs = gigsSearchByCategory(search_query=selected_category)
        for gig in gigs:
            result_hits.append(gig)
            logger.info(f"gigsByCategory() Method: Gigs By Category Found for {selected_category}")
            response = {
                'Message': 'Gigs By Category Found',
                'gigs': result_hits,
            }
            return(jsonify(response)), HTTPStatus.OK
    except Exception as err:
        logger.error(f"Error in gigsByCategory() Method : {str(err)}")
        return jsonify('Gigs By Category were not found')
    

@getgig_blueprint.route('/getmore-gig/<string:gig_id>', methods=['GET'])
@jwt_required
def moreLikeThis(gig_id: str):
    try:
        result_hits = []
        gigs = getMoreGigsLikeThis(gig_id=gig_id)
        print('Gigs Are :', gigs)
        for gig in gigs['hits']['hits']:
            gig_source = gig['_source']
            result_hits.append(gig_source)
        print('Result_Hits :', result_hits)
        logger.info(f"moreLikeThis() Method: More like this Found for {gig_id}")
        response = {
            'Message': 'More Like This Found',
            'gigs': result_hits,
        }
        return(response), HTTPStatus.OK    
    except Exception as err:
        logger.error(f"Error in moreLikeThis() Method : {str(err)}")
        return jsonify('More like this were not found')
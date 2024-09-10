from flask import request, Blueprint, jsonify
from Services_GIg.gig_service import seedData
from Helper_Gig.verify_token import jwt_required
from Queues_Gig.gig_producer import startPublishGigs
from Helper_Gig.logHandler import logger
import json

seedgig_blueprint = Blueprint('Gig_Seed', __name__, url_prefix='/api/v1/gig')


@seedgig_blueprint.route('/seed-gig/<int:count>', methods=['POST'])
@jwt_required
def seed(count: int):
    try:
        body={
            'count': str(count),
            'type': 'get_sellers'
        }
        startPublishGigs(exchange_name='', routing_key='user-gig-seed', body=body)
        logger.info("Publishing Message for the user Service to Get Sellers")
        return(jsonify("Seed() Method: Gigs were Seeded"))
    except Exception as err:
        logger.error(f"Error in seed() Method : {str(err)}")
        return(jsonify('Seed() Method, GIgs Could not be seeded'))
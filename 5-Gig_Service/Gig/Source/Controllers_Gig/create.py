from Helper_Gig.logHandler import logger
from Services_GIg.gig_service import createGig
from Helper_Gig.verify_token import jwt_required
from Helper_Gig.elastic import elastic_connection
from http import HTTPStatus
from flask import request, Blueprint
import json
creategig_blueprint = Blueprint('Create_Gig', __name__, url_prefix='/api/v1/gig')



@creategig_blueprint.route('/create-gig', methods=['POST'])
@jwt_required
def gigCreate():
    # to create Validation we can create Gig form when we program the frontend and then validate the form 
    # The cover Image for the gig will be handled in the API Service
    try:
        count = elastic_connection.getDocumentCount('gigs')
        gig_data = {
            'sellerId': request.get_json()['seller_id'],
            'username': request.get_json()['username'],
            'email': request.get_json()['email'],
            'profilePicture': request.get_json()['profile_pic'],
            'title': request.get_json()['title'],
            'description': request.get_json()['description'],
            'categories': request.get_json()['categories'],
            'subCategories': [request.get_json()['sub_categories']],
            'tag': [request.get_json()['tag']],
            'price': request.get_json()['price'],
            'expectedDelivery': request.get_json()['expected_delievery'],
            'basicTitle': request.get_json()['title'],
            'basicDescription': request.get_json()['description'],
            'coverImage': request.get_json()['cover_image'],
            'sortId': count + 1, 
        }
        gig = createGig(gig_data)
        response = {
            'Message': 'Gig Created Successfully',
            'GIg': gig.as_dict(),
        }
        return(response), HTTPStatus.OK  
    except Exception as err:
        logger.error(f"Error in gigCreate() Method {str(err)}")
        return('Could net Create Gig')
    
from Helper_Gig.logHandler import logger
from Services_GIg.gig_service import updateGig, updateActiveGig
from Helper_Gig.verify_token import jwt_required
from http import HTTPStatus
from flask import request, Blueprint
import json
updategig_blueprint = Blueprint('Update_Gig', __name__, url_prefix='/api/v1/gig')



@updategig_blueprint.route('/update-gig/<string:id>', methods=['PUT'])
@jwt_required
def gigUpdate(id: int):
    # to create Validation we can create Gig Updateform when we program the frontend and then validate the form 
    # The cover Image for the gig will be handled in the API Service
    # Also Remmember to handle if the cover image for the gig is updated or not
    try:
        gig_data = {
            'title': request.get_json()['title'],
            'description': request.get_json()['description'],
            'categories': request.get_json()['categories'],
            'subCategories': [request.get_json()['sub_categories']],
            'tag': [request.get_json()['tag']],
            'price': request.get_json()['price'],
            'expectedDelivery': request.get_json()['expected_delievery'],
            'basicTitle': request.get_json()['basic_title'],
            'basicDescription': request.get_json()['basic_description'],
            'coverImage': request.get_json()['profile_pic'],
        }
        gig = updateGig(gig_id=id, gig_data=gig_data)
        logger.info(f"Gig {gig['title']} Updated Successfully")
        response = {
            'Message': 'Gig Updated Successfully',
            'GIg': gig,
        }
        return(response), HTTPStatus.OK  
    except Exception as err:
        logger.error(f"Error in gigUpdate() Method {str(err)}")
    

@updategig_blueprint.route('/updategig-active/<string:gig_id>', methods=['PUT'])
@jwt_required
def gigUpdateActive(gig_id: str):
    try:
        updated_gig = updateActiveGig(gig_id=gig_id, active=bool(request.get_json()['active']))
        logger.info(f"Gig {updated_gig.title} Active Status Updated Successfully")
        response = {
            'Message': 'Active Status Updated Successfully',
            'gig': updated_gig.as_dict(),
        }
        return(response), HTTPStatus.OK
    except Exception as err:
        logger.error(f"error in gigUpdateActive() Method {str(err)}")
                                  
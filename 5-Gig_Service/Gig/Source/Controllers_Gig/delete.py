from Helper_Gig.logHandler import logger
from Services_GIg.gig_service import deleteGig
from Helper_Gig.verify_token import jwt_required
from http import HTTPStatus
from flask import request, Blueprint
import json

deletegig_blueprint = Blueprint('Delete_Gig', __name__, url_prefix='/api/v1/gig')



@deletegig_blueprint.route('/delete-gig/<string:gig_id>/<string:seller_id>', methods=['DELETE'])
@jwt_required
def gigDelete(gig_id: str, seller_id: str):
    try:
        print('Seller_id is :', seller_id)
        print('Gig Id is', gig_id)
        deleteGig(gig_id=gig_id, seller_id=seller_id)
        logger.info(f"Gig Deleted Successfully")
        response = {
            'Message': 'Gig Deleted Successfully',
        }
        return(response), HTTPStatus.OK  
    except Exception as err:
        logger.error(f"Error in delete gig() Method {str(err)}")
    
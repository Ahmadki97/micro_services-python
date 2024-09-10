from flask import request, jsonify, Blueprint
from Models_Users.seller_form import SellerForm
from Helper_Users.errorhandlers import BadRequestError
from Helper_Users.verify_token import jwt_required
from Services.seller_service import updateSeller
from http import HTTPStatus


update_seller_blueprint = Blueprint("Update_Seller", __name__, url_prefix='/api/v1/users/sellers')


@update_seller_blueprint.route('/updateseller-id/<string:id>', methods=['PUT'])
@jwt_required
def update_seller(id):
    # We should add seller Form Checks when building the Frontend
    if request.method == 'PUT':
        data = request.get_json()
        seller = updateSeller(id, data)
        response = {
            'Message': 'Seller Updated Successfully',
            'Seller': seller.as_dict(),
            'HTTP_Status': HTTPStatus.OK
        }
        return jsonify(response)
    else:
        raise BadRequestError('Request Should be POST Method')
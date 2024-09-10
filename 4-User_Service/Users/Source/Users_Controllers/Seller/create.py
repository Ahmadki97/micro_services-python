from Services.seller_service import createSeller, getSellerByEmail
from Helper_Users.verify_token import jwt_required
from Helper_Users.errorhandlers import BadRequestError
from Models_Users.seller_form import SellerForm
from flask import request, Blueprint

create_seller_blueprint = Blueprint('Create_Seller', __name__, url_prefix='/api/v1/users/sellers')

@create_seller_blueprint.route('/create-seller', methods=['POST'])
@jwt_required
def seller():
    if request.method == 'POST':
        seller_form = SellerForm(request.form)
        if seller_form.validate():
            seller = getSellerByEmail(request.get_json()['email'])
            if seller is not None:
                raise BadRequestError("Seller already exists", "seller() Method Error")
            else:
                seller_data = {
                    'profile_pic_id': request.get_json()['profile_pic_id'],
                    'full_name': request.get_json()['full_name'],
                    'username': request.get_json()['username'],
                    'email': request.get_json()['email'],
                    'profile_pic': request.get_json()['profile_pic'],
                    'description': request.get_json()['description'],
                    'onliner': request.get_json()['onliner'], 
                    'country': request.get_json()['country'],
                    'skills': request.get_json()['skills'],
                    'languages': request.get_json()['languages'],
                    'response_time': request.get_json()['response_time'], 
                    'experience': request.get_json()['experience'],
                    'education': request.get_json()['education'],
                    'social_links': request.get_json()['social_links'],
                    'certificates': request.get_json()['certificates'],
                }
                createSeller(seller_data)
        else:
             error_message = "The following fields have errors:\n"
             for field, errors in seller_form.errors.items():
                error_message += f"{field}: {', '.join(map(str, errors))}\n"
             raise BadRequestError(error_message, "seller() Method Error")



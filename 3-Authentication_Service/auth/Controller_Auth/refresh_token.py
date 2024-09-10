from flask import request, jsonify, Blueprint
from Helper_Auth.verify_token import jwt_required
from Services_Auth.auth_service import Routes
from http import HTTPStatus


refresh_token_blue_print = Blueprint('Search', __name__, url_prefix='/api/v1/auth')

@refresh_token_blue_print.route('', methods=['PUT'])
@jwt_required
def refreshToken():
    username = request.args.get('username')
    user = Routes.getAuthUserByUsername(username)
    user_token = Routes.signToken(id=user.id, username=username, email=user.email)
    response = {
        'message': 'Token Refreshed',
        'HTTP_Status': HTTPStatus.OK,
        'user': dict(user),
        'token': user_token
    }
    return jsonify(response)

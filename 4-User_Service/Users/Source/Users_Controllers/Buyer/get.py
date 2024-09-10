from flask import request, jsonify, Blueprint
from http import HTTPStatus
from Services.buyer_services import getBuyerByEmail, getBuyerByUsername
from Helper_Users.verify_token import jwt_required
from flask_login import current_user


buyer_blue_print = Blueprint('buyer', __name__, url_prefix='/api/v1/users/buyers')


@buyer_blue_print.route('/getbuyer-email', methods=['GET'])
@jwt_required
def email():
    buyer = getBuyerByEmail(request.get_json()['email'])
    print(buyer.username)
    response = {
        'message': 'Buyer Found',
        'buyer': buyer.username,
        'Http_Status': HTTPStatus.OK,
    }
    return jsonify(response)


@buyer_blue_print.route('/username', methods=['GET'])
@jwt_required
def currentUsername():
    buyer = getBuyerByUsername(request.current_user.username)
    response = {
        'message': 'Buyer Found',
        'buyer': buyer,
        'Http_Status': HTTPStatus.OK,
    }
    return jsonify(response)


@buyer_blue_print.route('/getbuyer-username', methods=['GET'])
@jwt_required
def username():
    buyer = getBuyerByUsername(request.get_json()['username'])
    print(buyer.username)
    response = {
        'message': 'Buyer Found',
        'buyer': buyer.username,
        'Http_Status': HTTPStatus.OK,
    }
    return jsonify(response)
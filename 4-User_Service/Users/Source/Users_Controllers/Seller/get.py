from Services.seller_service import getSellerById, getSellerByusername, getRandomSellers
from Helper_Users.verify_token import jwt_required
from flask import request, Blueprint, jsonify
from http import HTTPStatus
import json

get_seller_blueprint = Blueprint("Get_Seller", __name__, url_prefix='/api/v1/users/sellers')


@get_seller_blueprint.route('/getseller-id/<string:id>', methods=['GET'])
@jwt_required
def getSellerId(id):
    seller = getSellerById(id)
    print('Seller Fullname is :' ,seller.fullname)
    response = {
        'Message': 'Seller Found',
        'Seller': seller.as_dict(),
        'HTTP_STATUS': HTTPStatus.OK,
    }
    return jsonify(response)


@get_seller_blueprint.route('/getseller-username/<string:username>', methods=['GET'])
@jwt_required
def getSellerUsername(username: str):
    seller = getSellerByusername(username)
    response = {
        'Message': 'Seller Found',
        'Seller': seller.as_dict(),
        'HTTP_Status': HTTPStatus.OK,
    }
    return jsonify(response)


@get_seller_blueprint.route('/getseller-random/<int:count>', methods=['GET'])
@jwt_required
def getSellerRandom():
    sellers = getRandomSellers(request.args.count)
    response = {
        'Message': 'Seller Found',
        'Selelr': dict(sellers),
        'HTTP_Status': HTTPStatus.OK,
    }
    return jsonify(response)

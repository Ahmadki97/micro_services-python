from flask import request, jsonify, Blueprint
from Helper_Auth.verify_token import jwt_required
from Helper_Auth.errorhandlers import BadRequestError
from Queus_Auth.publish import startPublishAuth
from Services_Auth.auth_service import Routes
from dotenv import load_dotenv
from http import HTTPStatus
import secrets
import os 
import json


current_user_routes = Blueprint('Current_User', __name__, url_prefix='/api/v1/auth')
load_dotenv('.env')

@current_user_routes.route('/current-user', methods=['GET'])
@jwt_required
def currentUser():
    user = None
    existing_user = Routes.getAuthUserByID(request.current_user.id)
    if existing_user and len(existing_user) > 0:
        user = existing_user    
    response = {
        'message': 'Authenticated User',
        'user': user
    }
    return jsonify(response), HTTPStatus.OK


@current_user_routes.route('/resend-email', methods=['GET'])
@jwt_required
def resendEmail():
    email = request.get_json()['email']
    id = request.get_json()['id']
    user = Routes.getAuthUserByEmail(email)
    if user is None:
        raise BadRequestError('Email is invalid', 'Error in current_user resendEmail() Method..')
    else:
        token = secrets.token_hex(20)
        verification_link = f"{os.getenv('CLIENT_URL')}/confirm_email?v_token={token}"
        Routes.updateAuthUserEmailVerified(id=id, email_verified=0, email_verification_token=token)
        message = {
            'reciever_email': email,
            'verification_link': verification_link,
            'Template:': ''
        }
        startPublishAuth(queue='auth_user', exchange_name='', routing_key='auth_user', body=json.dumps(message))
        return jsonify('Email Verification Sent..'), HTTPStatus.OK, jsonify(message), jsonify(dict(user))
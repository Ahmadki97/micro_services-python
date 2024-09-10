from flask import request, jsonify, Blueprint
from Helper_Auth.logHandler import logger
from Helper_Auth.errorhandlers import BadRequestError
from Queus_Auth.publish import startPublishAuth
from Services_Auth.auth_service import Routes
from Helper_Auth.verify_token import jwt_required
from dotenv import load_dotenv
import secrets
import os
import json 

signup_route = Blueprint('Signup', __name__, url_prefix='/api/v1/auth')
load_dotenv('.env')


@signup_route.route('/signup', methods=['POST'])
@jwt_required
def signup():
    try:
        data = request.get_json() 
        print('Data in the request: ', data)
        if not data or 'email' not in data or 'password' not in data:
            return('There is no data in the request')
        else:
            username = request.get_json()['username']
            email = request.get_json()['email']
            if Routes.getAuthUserByUsername(username) or Routes.getAuthUserByEmail(email):
                logger.error('Invalid Credintials username or email', 'signup() Method Error')
                raise BadRequestError('Invalid Credintials username or email', 'signup() Method Error')
            else:
                auth_user_data = {
                    'username': username,
                    'email': email,
                    'password': request.get_json()['password'],
                    'country': request.get_json()['country'],
                    'profile_pic': request.get_json()['profile_pic'],
                    'email_verification_token': secrets.token_hex(20), 
                }
                body = {
                    'reciever_email': email,
                    'verify_link': f"{os.getenv('CLIENT_URL')}/confirm_email?v_token={auth_user_data['email_verification_token']}" ,
                }
                print("User Data is :", auth_user_data)
                Routes.createAuthUser(data=auth_user_data)
                print('Message For Notification Service is : ', json.dumps(body))
                startPublishAuth(queue='register', exchange_name='', routing_key='register', body=json.dumps(body))
                return(jsonify("Auth User Created Successfully"))
    except Exception as err:
        logger.error(f"Error in signup() Function {str(err)}")
        return(jsonify("Could Not Create Auth User"))

# Check How to initialize Configuration Link
# 
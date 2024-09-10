from flask import request, jsonify, session, Blueprint
from Services_Auth.auth_service import Routes
from dotenv import load_dotenv
from Helper_Auth.verify_token import jwt_required
from Helper_Auth.errorhandlers import BadRequestError
from Helper_Auth.verify_email import isValidEmail
from Helper_Auth.logHandler import logger
from Queus_Auth.publish import startPublishAuth
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os 
import secrets
import json

change_password_routes = Blueprint('Auth_change_password', __name__, url_prefix='/api/v1/auth')


load_dotenv('.env')


@change_password_routes.route('/reset-token', methods=['PUT'])
@jwt_required
def resetPasswordToken():
    try:
        email = request.get_json()['email']
        if isValidEmail(email):
            user = Routes.getAuthUserByEmail(email)
            if user is None:
                raise BadRequestError('Invalid Email','Error in resetPasswordToken() Method')
            else:
                token = secrets.token_hex(20)
                date = datetime.now() + timedelta(hours=1)
                Routes.updateAuthUSerPasswordToken(id=user.id, token=token, date=date)
                logger.info(f" Updating Reset Password token for user {user.username}, resetPasswordToken() Method")
                reset_link = f"{os.getenv('CLIENT_URL')}/reset_password?token={token}"
                message = {
                    "reciever_email": user.email,
                    "reset_link": reset_link,
                    "username": user.username,
                }

                startPublishAuth(queue='password', exchange_name='', routing_key='password', body=json.dumps(message))
                logger.info("Sending Message for the Notification Service, resetPasswordToken() Method ")
                return(jsonify("Reset Password Link is sent for your Email"))
    except Exception as err:
        logger.error(f"Error in resetPasswordToken(), {str(err)}")
        return(jsonify("Could Not send Reset Password Link for the User Email"))


@change_password_routes.route('/reset-password', methods=['PUT'])
@jwt_required
def resetPassword():
    token = request.args.get('token')
    password = request.get_json()['password']
    password_confirm = request.get_json()['confirm_password']
    if password == password_confirm:
        user = Routes.getAuthUserByPasswordToken(token)
        if user is not None:
            logger.info(f"Upating Password for user {user.username}, resetPassword() Method .")
            Routes.updateAuthUSerPassword(user.id, password)
            message = {
                'username': user.username,
                'templated': 'Template'
            }
            startPublishAuth(queue='password', exchange_name='', routing_key='password', body=json.dumps(message))
            logger.info('Sending Message Details to notification Service, resetPassword() Method.')
            return(jsonify("Password Reseted"))
        else:
            raise BadRequestError('Reset Token has Expired', 'resetPassword() Method Error.')
    else:
        raise BadRequestError('Password do not match', 'resetPassword() Method Error.')


@change_password_routes.route('/change-password/<int:id>', methods=['PUT'])
@jwt_required
def changePassword():
    new_password = request.get_json()['password']
    user = Routes.getAuthUserByUsername(session.get('user'))
    if user is None:
        raise BadRequestError('Invalid password','Error in changePassword() Method .')
    else:
        if user.verifyPassword(new_password):
            raise BadRequestError('Invalid Password', 'Error in changePassword() Method .')
        else:
            Routes.updateAuthUSerPassword(user.id, new_password)
            message = {
                'username': user.username,
                'Templates': ''
            }
            startPublishAuth(queue='auth', exchange_name='', routing_key='auth', body=json.dumps(message))
            return(jsonify('Password has Changed Succesfully..'))
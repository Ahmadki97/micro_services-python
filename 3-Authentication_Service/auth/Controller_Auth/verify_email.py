from flask import request, jsonify, Blueprint
from Services_Auth.auth_service import Routes
from dotenv import load_dotenv
from Helper_Auth.verify_token import jwt_required
from Helper_Auth.errorhandlers import BadRequestError
from Helper_Auth.logHandler import logger
import os 

verify_email_route = Blueprint('VerifyEmail', __name__, url_prefix='/api/v1/auth')
load_dotenv('.env')


@verify_email_route.route('/verify-email', methods=['PUT'])
@jwt_required
def verifyEmail():
    try:
        email_verified = bool(int(request.get_json()['email_verified']))
        print('email_status :', email_verified)
        user =  Routes.getAuthUserByVerificationToken(request.get_json()['email_verification_token'])
        print('user :', user)
        if user is None:
                raise BadRequestError("Verification Token is either invalid or is already used", "verifyEmail() Method")
        else:
            Routes.updateAuthUserEmailVerified(user.id, email_verified, '')
            logger.info(f"Email Verified Succesfully for User with id {user.id}")
            return(jsonify(f"Email Verified Succesfully for User with id {user.id}"))
    except Exception as err:
        logger.error(f"Error in verifyEmail() Method : {str(err)}")
        print('the Error is :', str(err))
        return(str(err))

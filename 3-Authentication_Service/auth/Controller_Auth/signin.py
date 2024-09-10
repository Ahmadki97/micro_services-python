from flask import request, jsonify, Blueprint
from Helper_Auth.verify_token import jwt_required
from Helper_Auth.verify_email import isValidEmail
from Helper_Auth.verify_request import validateRequest
from Helper_Auth.logHandler import logger
from Services_Auth.auth_service import Routes

signin_route = Blueprint('Signin', __name__, url_prefix='/api/v1/auth')

@signin_route.route('/signin', methods=['POST'])
@jwt_required
def signIn():
    try:
        if validateRequest():
            email = request.get_json()['email']
            print('Email is :', email)
            passwd = request.get_json()['password']
            if isValidEmail(email):
                user = Routes.getAuthUserByEmail(email)
                if user.verifyPassword(passwd):
                    logger.info(f"User Credentials are valid signIn() Method")
                    Routes.signToken(id=user.id, username=user.username, email=user.email)
                    return(jsonify(f"User {user.username} Has Signed in"))
                else:
                    return(jsonify(f"User Password is incorrect"))  
        else:
            logger.error(f"User credentials are Not Valid signIn() Method")
            return(jsonify(f"User {email} Could Not Be Signed In"))
    except Exception as err:
        logger.error(f"Error in signIn() Method, {str(err)}")
        return(jsonify(f"User Could Not Be Signed In"))


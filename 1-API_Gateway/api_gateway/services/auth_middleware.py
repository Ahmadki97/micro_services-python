from functools import wraps
from flask import request, jsonify, g
from Helper_api.errorhandlers import NotAuthorizedError, BadRequestError
import jwt
from flask import current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt




def custom_jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"Headers in the request {request.headers}")
        print(F"Csrf token in the request is {request.cookies.get('csrf')}")
        verify = verify_jwt_in_request() # To Verify that JWT token is existed in the request
        if verify is None:
            raise NotAuthorizedError('Token is Not Available Please Login Again', 'Gateway Service verifyUser() Method')
        else:
            data = get_jwt()
            print(f"Data in JWT is {data}")
        if data is None:
            raise BadRequestError('Authentication is required to access this route.', 'GatewayService checkAuthentication() method error')
        return fn(*args, **kwargs)
    return wrapper ## To return the Function 

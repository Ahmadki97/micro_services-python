from functools import wraps
from flask import request, jsonify
from Helper_Auth.errorhandlers import NotAuthorizedError
import jwt
import os

def jwt_required(func):
    @wraps(func)
    def decoratedFunction(*args, **kwargs):
        tokens = ['auth', 'seller', 'gig', 'search', 'buyer', 'message', 'order', 'review']
        if 'Authorization' not in request.headers:
            raise NotAuthorizedError('Request Not Authorized', 'jwt_required(): Request not coming from API Gateway')
        
        auth_header = request.headers.get('Authorization')
        if not auth_header.startswith('Bearer '):
            raise NotAuthorizedError('Request Not Authorized', 'jwt_required(): Request not coming from API Gateway')
        token = auth_header.split(' ')[1]
        jwt_token = jwt.decode(token, key=os.getenv("GATEWAY_JWT_TOKEN"), algorithms='HS256')
        print('Request Headers is', request.headers)
        print('The Token is: ',jwt_token)
        payload = jwt_token.get('service_name')
        print('Payload is : ', payload)
        if payload not in tokens:
            raise NotAuthorizedError('Request Not Authorized', 'jwt_required(): Request PayLoad is invalid ')

        
        return func(*args, **kwargs)
    return decoratedFunction
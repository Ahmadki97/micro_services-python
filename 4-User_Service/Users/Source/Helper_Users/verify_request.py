from flask import request
from Helper_Users.errorhandlers import BadRequestError
from Models_Users.seller_schema import Seller


def validateRequest():
    data = request.get_json()
    
    print('Data in the request: ', data)
    if not data or 'username' not in data or 'password' not in data:
            raise BadRequestError('Invalid request Error', 'signIn() Method')
    else:
          return True
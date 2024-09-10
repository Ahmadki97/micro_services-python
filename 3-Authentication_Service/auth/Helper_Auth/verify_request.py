from flask import request
from Helper_Auth.errorhandlers import BadRequestError


def validateRequest():
    data = request.get_data().decode('utf-8')
    print('Data in the request: ', data)
    if not data or 'email' not in data or 'password' not in data:
            raise BadRequestError('Invalid request Error', 'signIn() Method')
    else:
          return True
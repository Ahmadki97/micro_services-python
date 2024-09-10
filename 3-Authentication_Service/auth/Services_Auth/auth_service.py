from flask import request, jsonify
from models import User
import json 
import jwt
import os
from Queus_Auth.publish import startPublishAuth
from Helper_Auth.logHandler import logger
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv


class Routes():
    @staticmethod
    def createAuthUser(data):
        try:
            from server import db
            user = User(**data)
            print("user password is :", user.password)
            print('User Emails is :', user.email)
            user.email = data['email']
            db.session.add(user)
            db.session.commit()
            message_details = {
                'username': user.username,
                'email': user.email,
                'profile_pic': user.profile_pic,
                'country': user.country,
                'created_at': user.created_at.isoformat(), # Iso Format is needed to be able to convert datetime to json 
                'type': 'auth'
            }
            startPublishAuth(queue='user-buyer', exchange_name='', routing_key='user-buyer', body=json.dumps(message_details))
            return True
        except Exception as err:
            logger.error(f"Error in CreateAuthUser() {str(err)}")
            logging.error(f"Error in CreateAuthUser() {str(err)}")
            return False
        
    @staticmethod
    def getAuthUserByID(id):
        try:
            from server import db 
            user = db.session.query(User).filter(User.id==id).first()
            if user is not None:
                logger.info(f"User With id {user.id} is found getAuthUserByID()")
                user_serialized = user.serialize()
                print('User info : ', user_serialized)
                return True
            else:
                logger.info(f"User with id {id} is not Found")
                return False
        except Exception as err:
            logging.error(f"Error in getAuthUserById() Function : {str(err)}")
            logger.error(f"Error in getAuthUserById() Function : {str(err)}")
            return False

    @staticmethod
    def getAuthUserByUsername(username):
        try:
            from server import db
            user = db.session.query(User).filter(User.username == username).first()
            if user is not None:
                logger.info(f"User With Username: {username} is found geAuthtUserByUsername()")
                return user
            else:
                logger.info(f"User with Username: {username} is not found getAuthUserByUsername()")
                return False
        except Exception as err:
            logging.error(f"error in getAuthUserByUsername() Function {str(err)}")
            logger.error(f"error in getAuthUserByUsername() Function {str(err)}")            
            return False

    @staticmethod
    def getAuthUserByEmail(email):
        try:
            from server import db
            user = db.session.query(User).filter(User.email == email).first()
            if user is not None:
                logger.info(f"User With Email: {email} is found geAuthtUserByEmail()")
                return user
            else:
                logger.info(f"User with Email: {email} is not found getAuthUserByEmail()")
                return False
        except Exception as err:
            logging.error(f"error in getAuthUserByEmail() Function {str(err)}")
            logger.error(f"error in getAuthUserByEmail() Function {str(err)}")            
            return False

    @staticmethod
    def getAuthUserByVerificationToken(verification_token):
        try:
            from server import db
            user = db.session.query(User).filter(User.email_verification_token == verification_token).first()
            if user is not None:
                logger.info(f"User With Email Verification Token: {verification_token} is found geAuthtUserByVerificationToken()")
                return user 
            else:
                logger.info(f"User with Email Verification Token: {verification_token} is not found getAuthUserByVerification Token()")
                return False
        except Exception as err:
            logging.error(f"error in getAuthUserByVerificationToken() Function {str(err)}")
            logger.error(f"error in getAuthUserByVerificationToken() Function {str(err)}")            
            return False

    @staticmethod
    def getAuthUserByPasswordToken(password_token):
        try:
            from server import db
            user = db.session.query(User).filter(User.password_reset_token == password_token and User.password_reset_expires > datetime.now()).first()
            if user is not None:
                logger.info(f"User With Password Reset Token: {password_token} is found geAuthtUserByPasswordToken()")
                return user
            else:
                logger.info(f"User with Password Reset Token: {password_token} is not found getAuthUserByPasswordToken()")
                return False
        except Exception as err:
            logging.error(f"error in getAuthUserByPasswordToken() Function {str(err)}")
            logger.error(f"error in getAuthUserByPasswordToken() Function {str(err)}")    
            return False

    @staticmethod
    def updateAuthUserEmailVerified(id, email_verified, email_verification_token):
        try:
            from server import db 
            user = db.session.query(User).filter(User.id == id).first()
            if user is not None:
                logger.info(F"updateAuthUserEmailVerified() {user.username} Info ")
                user.email_verified = email_verified
                user.email_verification_token = email_verification_token 
                db.session.commit()
                return user
            else:
                logger.error(f"User Not Found Error in updateAuthUserEmailVerified() for user with id {id}")
                logging.error(f"User Not Found Error in updateAuthUserEmailVerified() for user with id {id}")
                return False
        except Exception as err:
            logging.error(f"Error in updateAuthUserEmailVerified() for user with id: {id} : {str(err)}")
            logger.error(f"Error in updateAuthUserEmailVerified() for user with id: {id} : {str(err)}")
            return False
    
    @staticmethod
    def updateAuthUSerPasswordToken(id, token, date):
        try:
            from server import db 
            user = db.session.query(User).filter(User.id == id).first()
            if user is not None:
                logger.info(F"updateAuthUserPasswordToken() for User {user.username} Success")
                user.password_reset_token = token
                user.password_reset_expires = date
                db.session.commit()
                return(jsonify('Password Reset Token Updated Succefully'))
            else:
                logger.error(f"User Not Found Error in updateAuthUserPasswordToken() for user with id {id}")
                logging.error(f"User Not Found Error in updateAuthUserPasswordToken() for user with id {id}")
                return(jsonify("User With ID {id} Not Found"))
        except Exception as err:
            logging.error(f"Error in updateAuthUserPasswordToken() for user with id: {id} : {str(err)}")
            logging.error(f"Error in updateAuthUserPasswordToken() for user with id: {id} : {str(err)}")
            return(jsonify("Internal Server error 404"))

    @staticmethod
    def updateAuthUSerPassword(id, passwd):
        try:
            from server import db 
            user = db.session.query(User).filter(User.id == id).first()
            if user is not None:
                logger.info(F"updateAuthUserPassword() {user.username} Info ")
                user.password_set(passwd)
                db.session.commit()
                return(jsonify("Password Updated Successfully"))
            else:
                logger.error(f"User Not Found Error in updateAuthUserPassword() for user with id {id}")
                logging.error(f"User Not Found Error in updateAuthUserPassword() for user with id {id}")
                return(jsonify("User With ID {id} Not Found"))
        except Exception as err:
            logging.error(f"Error in updateAuthUserPassword() for user with id: {id} : {str(err)}")
            logging.error(f"Error in updateAuthUserPassword() for user with id: {id} : {str(err)}")
            return(jsonify("Internal Server error 404"))
        
    @staticmethod
    def signToken(id, username, email):
        try:
            load_dotenv('.env')
            print('JWT Token is :', os.getenv('JWT_Token'))
            payload = {
                'id':id,
                'username':username,
                'email':email,
                'exp':datetime.now() + timedelta(days=7)
            }
            jwt_token = jwt.encode(payload, os.getenv('JWT_TOKEN'), algorithm='HS256')
            print('New JWT token is : ', jwt_token)
            logging.info('Authentication Service signToken(), Token is Signed')
            logger.info('Authentication Service signToken(), Token is Signed')
            return(jwt_token)
        except Exception as err:
            logging.error(f"Error in Authentication Service signToken() : {str(err)}")
            logger.error(f"Error in Authentication Service signToken() : {str(err)}")
            return(jsonify("Internal Server Error 404"))

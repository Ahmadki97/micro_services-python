from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from Helper_Auth.logHandler import logger
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime 



db = SQLAlchemy()
# Here We can Define Our Classes 
class User(db.Model):
    __tablename__ = 'auth_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True, index=True)
    password = db.Column(db.String(50), nullable=False, unique=False)
    country = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, index=True)
    profile_pic = db.Column(db.String(100), nullable=False)
    email_verification_token = db.Column(db.String(255), nullable=True)
    email_verified = db.Column(db.Boolean, nullable=True, default=False)
    created_at = db.Column(db.Date, default=datetime.now())
    password_reset_token = db.Column(db.String(255), nullable=True)
    password_reset_expires = db.Column(db.Date, nullable=False, default=datetime.now())
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

    def __init__(self, password, username, country, profile_pic, email, email_verification_token):
        self.username= username
        self.profile_pic= profile_pic
        self.country= country
        self.email= email
        self.password_set(password)
        self.email_verification_token = email_verification_token

    def password_get(self):
        return self.password


    def password_set(self, passwd):
        self.password = generate_password_hash(passwd)


    def verifyPassword(self, passwd):
        print('User Pssword is : ', self.password, 'Enterd Hashed Password is : ', generate_password_hash(passwd))
        if check_password_hash(self.password,passwd):
            return True
        else:
            return False
        
        
    def isValidEmail(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)

       
    def serialize(self):
        return{
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "country": self.country,
            "email": self.email,
            "profile_pic":self.profile_pic,
            "email_verification_token": self.email_verification_token,
            "email_verified": self.email_verified,
            "created_at": self.created_at.isoformat(),
            "password_reset_token": self.password_reset_token,
            "password_reset_expires": self.password_reset_expires.isoformat(),
        }




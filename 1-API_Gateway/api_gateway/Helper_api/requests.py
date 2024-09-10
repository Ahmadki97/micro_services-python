from flask import request
from flask_jwt_extended import get_jwt
from dotenv import load_dotenv
from Helper_api.cloudinary import uploadCloudinaryFile
import jwt 
import os 
import requests
import json

load_dotenv('.env')


class Requests():
    def __init__(self, service_url):
        self.service_url = service_url
        self.key = os.getenv('GATEWAY_JWT_TOKEN')

    def getJwtToken(self, service_token):
        payload = {
            'service_name': service_token,
        }
        jwt_token = jwt.encode(payload, self.key, algorithm='HS256')
        return jwt_token
    
    
    def makeRequest(self,endpoint, service_token):
        print('URL of the Destination Service is :', self.service_url)
        jwt_token = self.getJwtToken(service_token=service_token)
        headers = {
            'Authorization': f"Bearer {jwt_token}",
            'Content-Type': 'application/json'
        }
        url = f"{self.service_url}/{endpoint}"
        data = dict(request.form)
        data['currentUser'] = get_jwt()
        if request.files:
            profile_pic = request.files.get('profile_pic')
            file = request.files.get('file')
            data = dict(request.form)
            if profile_pic is not None :
                image_url = uploadCloudinaryFile(profile_pic)
                data['profile_pic'] = image_url
            elif file is not None:
                file_url = uploadCloudinaryFile(file)
                data['file'] = file_url
            response = requests.request(
                method= request.method,
                url= url,
                headers= headers,
                json= data,
                params= request.args,
                cookies= request.cookies,
                allow_redirects= False
            )
        else:
            response = requests.request(
                method= request.method,
                url= url,
                headers= headers,
                json= data,
                params= request.args,
                cookies= request.cookies,
                allow_redirects= False
            )
        response.content.decode('utf-8')
        response_json = json.loads(response.content)
        return json.dumps(response_json)
    
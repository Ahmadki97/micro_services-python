from flask import jsonify, Blueprint
from Helper_api.requests import Requests
from Helper_api.elastic import logger
from Helper_api.errorhandlers import ServerError
from services.auth_middleware import custom_jwt_required
from dotenv import load_dotenv
import json
import os 



load_dotenv('.env')
service_url = os.getenv('MESSAGE_BASE_URL')
print(f"Service Url is : {service_url}")
base_url = f"{service_url}/api/v1/chat"
gig_client = Requests(service_url=base_url)
chat_blue_print = Blueprint('Chat', __name__, url_prefix='/api/v1/chat')


@chat_blue_print.route('/add-message', methods=['POST'])
@custom_jwt_required
def addMessage():
    try:
        response = gig_client.makeRequest(endpoint=f"add-message", service_token='chat')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in addMessage() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "addMessage() Function")


@chat_blue_print.route('/update-offer', methods=['PUT'])
@custom_jwt_required
def updateOffer():
    try:
        response = gig_client.makeRequest(endpoint=f"update-offer", service_token='chat')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in updateOffer() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "updateOffer() Function")
    

@chat_blue_print.route('/updatemessages-multiple', methods=['PUT'])
@custom_jwt_required
def markMultipleMessages():
    try:
        response = gig_client.makeRequest(endpoint=f"updatemessages-multiple", service_token='chat')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in markMultipleMessages() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "markMultipleMessages() Function")
    

@chat_blue_print.route('/updatemessages-single', methods=['PUT'])
@custom_jwt_required
def markSingleMessage():
    try:
        response = gig_client.makeRequest(endpoint=f"updatemessages-single", service_token='chat')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in markSingleMessages() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "markSingleMessages() Function")
    

@chat_blue_print.route('/get-conversation/<string:sender>/<string:receiver>', methods=['GET'])
@custom_jwt_required
def getConversation(sender: str, receiver: str):
    try:
        response = gig_client.makeRequest(endpoint=f"get-conversation/{sender}/{receiver}", service_token='chat')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in getConversation() Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getConversation() Function")
    

@chat_blue_print.route('/get-message/<string:sender>/<string:receiver>', methods=['GET'])
@custom_jwt_required
def getMessages(sender: str, receiver: str):
    try:
        response = gig_client.makeRequest(endpoint=f"get-message/{sender}/{receiver}", service_token='chat')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in getMessage ,Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getMessage() Function")


@chat_blue_print.route('/getlist-conversation/<string:username>', methods=['GET'])
@custom_jwt_required
def getUserConversationList(username: str):
    try:
        response = gig_client.makeRequest(endpoint=f"getlist-conversation/{username}", service_token='chat')
        response_json = json.loads(response)
        print(response_json['Message'])
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in getUserConversationList ,Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getUserConversationList() Function")
    

@chat_blue_print.route('/getuser-message/<string:conv_id>', methods=['GET'])
@custom_jwt_required
def getUserMessage(conv_id: str):
    try:
        response = gig_client.makeRequest(endpoint=f"getuser-message/{conv_id}", service_token='chat')
        return(jsonify(response))
    except Exception as err:
        logger.error(f"Error in getUserMessage ,Function, the Error is : {str(err)}")
        raise ServerError("Internal Server Error", "getUserMessage() Function")


    



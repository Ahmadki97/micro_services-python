from Helper_Chat.logHandler import logger
from Helper_Chat.verify_token import jwt_required
from Services_Chat.chat_services import getConversation, getMessages, getUserMessages, getUserConversationList
from flask import Blueprint
from http import HTTPStatus
import json



get_blueprint = Blueprint('Get_Chat Service', __name__, url_prefix='/api/v1/chat')


@get_blueprint.route('/get-conversation/<string:sender>/<string:receiver>', methods=['GET'])
@jwt_required
def conversation(sender: str, receiver: str):
    try:
        conv = getConversation(sender, receiver)
        logger.info(f"get Conversation Controller, Conversation{conv.id} found.")
        response = {
            "Message": f"Conversation Found {conv.as_dict()}",
            "HTTP Status": HTTPStatus.OK
        }
        return response
    except Exception as err:
        logger.error(f"Error in get Conversation Controller , {str(err)}")
        return(f"Could not found Conversation.")
    

@get_blueprint.route('/get-message/<string:sender>/<string:receiver>', methods=['GET'])
@jwt_required
def message(sender: str, receiver: str):
    try:
        msgs = getMessages(sender=sender, receiver=receiver)
        logger.info(f"get message controller, messages Found.")
        response = {
            "Messages": json.dumps(msgs, default=str),
            'Status': HTTPStatus.OK
        }
        return response
    except Exception as err:
        logger.error(f"Error in get message Controller, {str(err)}")
        return(f"Could not Find Message.")
    

@get_blueprint.route('/getlist-conversation/<string:username>', methods=['GET'])
@jwt_required
def userConversationList(username: str):
    try:
        msgs = getUserConversationList(username)
        print(f"Messags in the controller : {msgs}and the type is {type(message)}" )
        logger.info(f"get conversation list controller, conversation list found for user {username}.")
        response = {
            'Message': json.dumps(msgs, default=str),
            'Http Status': HTTPStatus.OK
        }
        return response
    except Exception as err:
        logger.error(f"Error in get converation list Controller, {str(err)}")
        return(f"Could not Find Conversation List.")
    

@get_blueprint.route('/getuser-message/<string:conv_id>', methods=['GET'])
@jwt_required
def userMessage(conv_id: str):
    try:
        msgs = getUserMessages(conv_id=conv_id)
        logger.info(f"get user messages controller, messages for conversation {conv_id} Found.")
        response = {
            "Messages": json.dumps(msgs, default=str),
            "Http Status": HTTPStatus.OK
        }
        return response
    except Exception as err:
        logger.error(f"Error in get user message Controller, {str(err)}")
        return(f"Could not Find Messages.")
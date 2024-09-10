from Services_Chat.chat_services import updateOffer, markManyMessagesAsRead, markMessageAsRead
from Helper_Chat.logHandler import logger
from flask import request, Blueprint
from http import HTTPStatus


update_blueprint = Blueprint('Update_Chat Service', __name__, url_prefix='/api/v1/chat')


@update_blueprint.route('/update-offer', methods=['PUT'])
def offer():
    try:
        msg_id = request.get_json()['message']
        msg_type = request.get_json()['type']
        msg = updateOffer(message_id=msg_id, type_offer=msg_type)
        logger.info(f"update offer controller, offer {msg_id} updated successfully.")
        return msg, HTTPStatus.OK 
    except Exception as err:
        logger.error(f"Error in update offer Controller : {str(err)}")
        return(f"Failed to update offer.")
    
@update_blueprint.route('updatemessages-multiple', methods=['PUT'])
def markMultipleMessages():
    try:
        msg_id = request.get_json()['messageId']
        senderUsername = request.get_json()['senderUsername']
        receiverUsername = request.get_json()['receiverUsername']
        markManyMessagesAsRead(sender=senderUsername, receiver=receiverUsername, msg_id=msg_id)
        logger.info(f"update many messages controller, Marked Many messages as read for conversation {msg_id}")
        response = {
            'Message': "Multiple Messages marked as Read",
            "Status": HTTPStatus.OK,
        }
        return response
    except Exception as err:
        logger.error(f"Error in update multi messages controller: {str(err)} ")
        return(f"Failed to update multi messages ")
    

@update_blueprint.route('updatemessages-single', methods=['PUT'])
def markSingleMessage():
    try:
        msg_id = request.get_json()['messageId']
        markMessageAsRead(msg_id)
        logger.info(f"update single message controller, marked message {msg_id} as read")
        response = {
            'Message': "Message Marked as Read",
            'Status': HTTPStatus.OK
        }
        return response
    except Exception as err:
        logger.error(f"Error in update single message controller: {str(err)}")
        return(f"Failed to update single message")

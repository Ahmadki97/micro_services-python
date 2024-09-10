from flask import request, jsonify, Blueprint
from Services_Chat.chat_services import addMessage, createConversation
from Helper_Chat.logHandler import logger
from Helper_Chat.cloudinary import uploadCloudinaryFile
from Helper_Chat.errorhandlers import BadRequestError
from Helper_Chat.verify_token import jwt_required
from http import HTTPStatus


create_blueprint = Blueprint('Create_Chat Servie', __name__, url_prefix='/api/v1/chat')



@create_blueprint.route('/add-message', methods=['POST'])
@jwt_required
def creteMessage():
    try:
        offer = {
            'gigTitle': request.get_json()['gigTitle'],
            'price': int(request.get_json()['price']),
            'description': request.get_json()['description'],
            'deliveryInDays': int(request.get_json()['deliveryInDays']),
            'oldDeliveryDate': request.get_json()['oldDeliveryDate'],
            'newDeliveryDate': request.get_json()['newDeliveryDate'],
        }
        message_data = {
            'conversationId': request.get_json()['conversationId'],
            'senderUsername': request.get_json()['senderUsername'],
            'receiverUsername': request.get_json()['receiverUsername'],
            'senderPicture': request.get_json()['senderPicture'],
            'receiverPicture': request.get_json()['receiverPicture'],
            'body': request.get_json()['body'],
            'file': request.get_json()['file'],
            'fileType': request.get_json()['fileType'],
            'fileSize': request.get_json()['fileSize'],
            'fileName': request.get_json()['fileName'],
            'gigId': request.get_json()['gigId'],
            'buyerId': request.get_json()['buyerId'],
            'sellerId': request.get_json()['sellerId'],
            'isRead': bool(int(request.get_json()['isRead'])),
            'hasOffer': request.get_json()['hasOffer'],
            'offer': offer
        }
        
        print (f"message sent to the addMessag function is {message_data}, and the type is {type(message_data)}")
        if 'hasConversationId' not in request.get_json():
            createConversation(conv_id=message_data['conversationId'], sender=message_data['senderUsername'], receiver=message_data['receiverUsername'])
        addMessage(message=message_data)
        response = {
            "Message": "Message is created Successfully",
            "Http Status": HTTPStatus.OK
        }
        return response 
    except Exception as err:
        logger.error(f"Error in createMessage() Controller : {str(err)}")
        return(f"Could not Send/create Message")
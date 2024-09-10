from Helper_Chat.logHandler import logger
from Models_Chat.conversation_schema import Conversation
from Models_Chat.message_schema import Message
from Queues_Chat.chat_producer import startPublish
from mongoengine import ValidationError
from Sockets_Chat.sockets_io import sio
import json


def createConversation(conv_id: str, sender: str, receiver: str):
    try:
        conversation = Conversation(conversationId = conv_id, senderUsername = sender, receiverUsername = receiver)
        conversation.save()
        logger.info(f"createConversation() Method : conversation with id {conv_id} Created successfully.")
        return conversation
    except Exception as err:
        logger.error(f"Error in createConversation() Method : {str(err)}")
        return("createConversation() Method, Failed to Create Conversation.")

def addMessage(message: dict):
    try:
        print(f"Type of param is : {type(message)}")
        msg = Message(**message)
        print(msg)
        msg.validate()
        msg.save()
        logger.info(f"addMessage() Method, Message with id {msg.id} added successfully..")
        print(f"Message type is {type(msg)}, in the Services")
        print(f"Offer gig title is {message['offer']['gigTitle']}")
        if message['hasOffer'] is not None:
            queue_message = {
                'sender': message['senderUsername'],
                'amount': message['offer']['price'],
                'buyerUsername': message['receiverUsername'],
                'sellerUsername': message['senderUsername'],
                'title': message['offer']['gigTitle'],
                'description': message['offer']['description'],
                'deliveryDays': message['offer']['deliveryInDays'],
                'template': ''
            }
            startPublish(exchange_name='', routing_key='order-email', body=json.dumps(queue_message), service_name='Notification Service')
        sio.emit(event='message received', data=msg.as_dict())
        logger.info(f"Sending Message to API SocketIO")
        return msg.as_dict()
    except Exception or ValidationError as err:
        logger.error(f"Error in addMessage() Method : {str(err)}")
        return(f"Failed to Add Message.")


def getConversation(senderUsername: str, receiverUsername: str):
    try:
        conv = Conversation.objects.get(senderUsername=senderUsername, receiverUsername=receiverUsername) or Conversation.objects.get(receiverUsername=senderUsername, senderUsername=receiverUsername)
        print(f" Conversation is {conv} and type of conv is {type(conv)}")
        logger.info(f"Conversation With id {conv.id} Found.")
        return conv
    except Exception as err:
        logger.error(f"Error in getConversation() Method : {str(err)}")
        return(f"Failed to get Conversation.")
    

def getUserConversationList(username: str):
    try:
        pipeline = [
            {"$match": {"$or": [{"senderUsername": username}, {"receiverUsername": username}]}},
            {"$group": {
                "_id": "$conversationId",
                "result": {"$last": "$$ROOT"}
            }},
            {"$project": {
                "_id": "$result.Id",
                "conversationId": "$result.conversationId",
                "sellerId": "$result.sellerId",
                "buyerId": "$result.buyerId",
                "receiverUsername": "$result.receiverUsername",
                "receiverPicture": "$result.receiverPicture", 
                "senderUsername": "$result.senderUsername",
                "senderPicture": "$result.senderPicture",
                "body": "$result.body",
                "file": "$result.file",
                "gigId": "$result.gigId",
                "isRead": "$result.isRead",
                "hasOffer": "$result.hasOffer",
                "createdAt": "$result.createdAt"
            }}
        ]
        messages = Message.objects.aggregate(pipeline)
        messages_list = list(messages)
        print(f"Messages is {list(messages)}")
        logger.info(f"Conversation for user {username} Found.")
        return messages_list
    except Exception as err:
        logger.error(f"Error in getUserConversationList() Method : {str(err)}")
        return(f"Failed to get Conversation for user {username}")


def getMessages(sender: str, receiver: str):
    try:
        msgs = Message.objects.filter(senderUsername=sender, receiverUsername=receiver).order_by('+createdAt') 
        print(msgs)
        logger.info(f"getMessages() Method, Messgaes for users {sender} and {receiver} Found")
        response = []
        for msg in msgs:
            response.append(msg.to_mongo().to_dict())
        return response
    except Exception as err:
        logger.error(f"Error in getMessages() Method : {str(err)}")
        return(f"Faield to get Messages for users {sender,receiver}")
    

def getUserMessages(conv_id: str):
    try:
        msgs = Message.objects.filter(conversationId=conv_id)
        logger.info(f"getUserMessages() Method, messages for the conersation {conv_id} Successfully Found")
        messages = []
        for msg in msgs:
            messages.append(msg.to_mongo().to_dict())
        return messages
    except Exception as err:
        logger.error(f"Error in getUserMessages() Method: {str(err)}") 
        return(f"Faield to get Messages from Conversation {conv_id}")


def updateOffer(message_id: str, type_offer: str):
    try:
        Message.objects(id=message_id).modify(**{f"set__offer__{type_offer}": True})
        modified_msg = Message.objects.get(id=message_id)
        print(f"Type of Message is {type(modified_msg)}")
        logger.info(f"updateOffer() Method, the messgae with id {modified_msg.id} updated successfully")
        return modified_msg.as_dict()
    except Exception as err:
        logger.error(f"Error in updateOffer() Method, {str(err)}")
        return(f"Failed to update the message with id {message_id}.")


def markMessageAsRead(msg_id: str):
    try:
        msg = Message.objects.get(id=msg_id).modify(set__isRead=True)
        msg.reload()
        logger.info(f"markMessageAsRead() Method, Message with id {msg['_id']} is Read Successfully.")
        sio.emit(event='message updated', data=msg.as_dict())
        logger.info(f"Sending Message to API SocketIO")
    except Exception as err:
        logger.error(f"Error in markMessageAsread() Method : {str(err)}")


def markManyMessagesAsRead(sender: str, receiver: str, msg_id: str):
    try:
        Message.objects(senderUsername=sender, receiverUsername=receiver).update(isRead=True)
        logger.info(f"markManyMessagesAsRead() Method, Messages for users {sender, receiver} Marker as read")
        msg = Message.objects.get(id=msg_id) 
        sio.emit(event='message updated', data=msg.as_dict())
        logger.info(f"Sending Message to API Socketio")
    except Exception as err:
        logger.error(f"Error in markManyMessagesAsread() Method : {str(err)}")
        return("Failed to Update Message Read Status")
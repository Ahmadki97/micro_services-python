from mongoengine import Document, StringField, IntField, BooleanField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField
import datetime

class Offer(EmbeddedDocument):
    gigTitle = StringField(default='', error_messages={
        'string': 'Conversation Id must be of type string'
    })
    price = IntField(default=0, error_messages={
        'Int': 'Conversation Id must be of type string'
    })
    description = StringField(default='')
    deliveryInDays = IntField(default=0)
    oldDeliveryDate = StringField(default='')
    newDeliveryDate = StringField(default='')
    accepted = BooleanField(default=False)
    cancelled = BooleanField(default=False)


    def as_dict(self):
        offer = {
            'gigTitle': self.gigTitle,
            'price': self.price,
            'description': self.description,
            'deliveryInDays': self.deliveryInDays,
            'oldDeliveryDate': self.oldDeliveryDate,
            'newDeliveryDate': self.newDeliveryDate,
            'accepted': self.accepted,
            'cancelled': self.cancelled
        }



class Message(Document):
    conversationId = StringField(required=True, index=True, error_messages={
        'required': 'Conversation Id is required',
        'string': 'Conversation Id must be of type string'
    })
    senderUsername = StringField(required=True, index=True, error_messages={
        'required': 'senderUsername Id is required',
        'string': 'senderUsername Id must be of type string'
    })
    receiverUsername = StringField(required=True, index=True, error_messages={
        'required': 'recieverUsername Id is required',
        'string': 'recieverUsername Id must be of type string'
    })
    senderPicture = StringField(required=True, error_messages={
        'required': 'senderPicture Id is required',
        'string': 'senderPicture Id must be of type string'
    })
    receiverPicture = StringField(required=True, error_messages={
        'required': 'receiverPicture Id is required',
        'string': 'receiverPicture Id must be of type string'
    })
    body = StringField(required=True, default='', error_messages={
        'string': 'Body must be of type string'
    })
    file = StringField(default='', error_messages={
        'string': 'File must be of type string'
    })
    fileType = StringField(default='', error_messages={
        'string': 'FileType must be of type string'
    })
    fileSize = StringField(default='', error_messages={
        'string': 'FielSize must be of type string'
    })
    fileName = StringField(default='', error_messages={
        'string': 'fileName must be of type string'
    })
    gigId = StringField(default='', error_messages={
        'string': 'gigId must be of type string'
    })
    buyerId = StringField(required=True, default='', error_messages={
        'required': 'BuyerId is required',
        'string': 'BuyerId must be of type string'
    })
    sellerId = StringField(required=True, default='', error_messages={
        'required': 'Seller Id is required',
        'string': 'Seller Id must be of type string'
    })
    isRead = BooleanField(default=False, error_messages={
        'string': 'isRead must be of type bool'
    })
    hasOffer = BooleanField(default=False, error_messages={
        'string': 'hasOffer must be of type bool'
    })
    offer = EmbeddedDocumentField(Offer, default=None)
    createdAt = DateTimeField(default=datetime.datetime.now)


    def as_dict(self):
        message = {
            'conversationId': self.conversationId,
            'senderUsername': self.senderUsername,
            'receiverUsername': self.receiverUsername,
            'senderPicture': self.senderPicture,
            'receiverPicture': self.receiverPicture,
            'body': self.body,
            'file': self.file,
            'fileType': self.fileType,
            'fileSize': self.fileSize,
            'fileName': self.fileName,
            'gigId': self.gigId,
            'buyerId': self.buyerId,
            'sellerId': self.sellerId,
            'isRead': self.isRead,
            'offer': self.offer.as_dict()
        }
        return message


    

    
    
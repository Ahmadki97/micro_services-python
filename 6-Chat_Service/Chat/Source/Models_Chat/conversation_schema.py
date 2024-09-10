from mongoengine import Document, StringField


class Conversation(Document):
    conversationId = StringField(required=True, index=True, error_messages={
        'required': 'Conversation Id is required',
        'string': 'Conversation Id must be of type string'
    })
    senderUsername = StringField(required=True,unique=True, index= True, error_messages={
        'required': 'senderUsername Id is required',
        'string': 'senderUsername Id must be of type string'
    })
    receiverUsername = StringField(required=True,index=True, error_messages={
        'required': 'senderUsername Id is required',
        'string': 'senderUsername Id must be of type string'
    })


    def as_dict(self):
        conv = {
            'conversationId': self.conversationId,
            'senderUsername': self.senderUsername,
            'receiverUsername': self.receiverUsername
        }
        return conv

    
    
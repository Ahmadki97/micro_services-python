from mongoengine import Document, StringField, BooleanField, DateTimeField
import datetime

class Notification(Document):
    userTo = StringField(default='', index=True)
    senderUsername = StringField(default='')
    senderPicture = StringField(default='')
    receiverUsername = StringField(default='')
    receiverPicture = StringField(default='')
    isRead = BooleanField(default=False)
    message = StringField(default='')
    orderId = StringField(default='')
    createdAt = DateTimeField(default=datetime.datetime.now)


    def as_dict(self):
        notification = {
            'userTo': self.userTo,
            'senderUsername': self.senderUsername,
            'senderPicture': self.senderPicture,
            'receiverUSername': self.senderUsername,
            'receiverPicture': self.senderPicture,
            'isRead': self.isRead,
            'message': self.message,
            'orderId': self.orderId,
            'createdAt': self.createdAt,
        }
        return notification
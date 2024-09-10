from mongoengine import Document, StringField, IntField, BooleanField, DateTimeField, ListField, EmbeddedDocument, EmbeddedDocumentField
import datetime

class DeliveredWork(EmbeddedDocument):
    message = StringField()
    file = StringField()
    fileType = StringField()
    fileSize = StringField()
    fileName = StringField()

    def as_dict(slef):
        delivered_work = {
            "message":slef.message,
            "file":slef.file,
            "fileType":slef.fileType,
            "fileSize":slef.fileSize,
            "fileName":slef.fileName,
        }
        return delivered_work

class Offer(EmbeddedDocument):
    gigTitle = StringField(required=True)
    price = IntField(required=True)
    description = StringField(required=True)
    deliveryInDays = IntField(required=True)
    oldDeliveryDate = DateTimeField()
    newDeliveryDate = DateTimeField()
    accepted = BooleanField(required=True)
    cancelled = BooleanField(required=True)
    reason = StringField(default='')

    def as_dict(self):
        offer = {
            "gigTitle": self.gigTitle,
            "price": self.price,
            "description": self.description,
            "deliveryInDays": self.deliveryInDays,
            "oldDeliveryDate": self.oldDeliveryDate,
            "newDeliveryDate": self.newDeliveryDate,
            "accepted": self.accepted,
            "cancelled": self.cancelled,
            "reason": self.reason
        }
        return offer

class Events(EmbeddedDocument):
    placeOrder = DateTimeField()
    requirements = DateTimeField()
    orderStarted = DateTimeField()
    deliveryDateUpdate = DateTimeField()
    orderDelivered = DateTimeField()
    buyerReview = DateTimeField()
    sellerReview = DateTimeField()

    def as_dict(self):
        event = {
            "placeOrder": self.placeOrder,
            "requirements": self.requirements,
            "orderStarted": self.orderStarted,
            "deliveryDateUpdate": self.deliveryDateUpdate,
            "orderDelivered": self.orderDelivered,
            "buyerReview": self.buyerReview,
            "sellerReview": self.sellerReview
        }
        return event

class RequestExtension(EmbeddedDocument):
    originalDate = StringField(default='')
    newDate = StringField(default='')
    days = IntField(default=0)
    reason = StringField(default='')

    def as_dict(self):
        request_extension = {
            "originalDate": self.originalDate,
            "newDate": self.newDate,
            "days": self.days,
            "reason": self.reason
        }
        return request_extension

class Review(EmbeddedDocument):
    rating = IntField(default=0)
    review = StringField(default='')
    created = DateTimeField()

    def as_dict(self):
        review = {
            "rating": self.rating,
            "review": self.review,
            "created": self.created
        }
        return review


class Order(Document):
    offer = EmbeddedDocumentField(Offer, required=True)
    gigId = StringField(required=True)
    sellerId = StringField(required=True, index=True)
    sellerUsername = StringField(required=True)
    sellerImage = StringField(required=True)
    sellerEmail = StringField(required=True)
    gigCoverImage = StringField(required=True)
    gigMainTitle = StringField(required=True)
    gigBasicTitle = StringField(required=True)
    gigBasicDescription = StringField(required=True)
    buyerId = StringField(required=True)
    buyerUsername = StringField(required=True)
    buyerEmail = StringField(required=True)
    buyerImage = StringField(required=True)
    status = StringField(required=True)
    orderId = StringField(required=True, index=True)
    quantity = IntField(required=True)
    price = IntField(required=True)
    serviceFee = IntField(default=0)
    requirements = StringField(default='')
    approved = BooleanField(default=False)
    delivered = BooleanField(default=False)
    cancelled = BooleanField(default=False)
    approvedAt = DateTimeField()
    paymentIntent = StringField()
    deliveredWork = ListField(EmbeddedDocumentField(DeliveredWork))
    requestExtension = EmbeddedDocumentField(RequestExtension)
    dateOrdered = DateTimeField(default=datetime.datetime.now)
    events = EmbeddedDocumentField(Events)
    buyerReview = EmbeddedDocumentField(Review)
    sellerReview = EmbeddedDocumentField(Review)

    def as_dict(self):
        order = {
            'offer': self.offer.as_dict(),
            'gigId': self.gigId,
            'sellerId': self.sellerId,
            'sellerUsername': self.sellerUsername,
            'sellerEmail': self.sellerEmail,
            'sellerImage': self.sellerImage,
            'gigCoverImage': self.gigCoverImage,
            'gigMainTitle': self.gigMainTitle,
            'gigBasicTitle': self.gigBasicTitle,
            'gigBasicDescription': self.gigBasicDescription,
            'buyerId': self.buyerId,
            'buyerUsername': self.buyerUsername,
            'buyerImage': self.buyerImage,
            'buyerEmail': self.buyerEmail,
            'status': self.status,
            'orderId': self.orderId,
            'quantity': self.quantity,
            'price': self.price,
            'serviceFee': self.serviceFee,
            'requirements': self.requirements,
            'approved': self.approved,
            'delivered': self.delivered,
            'cancelled': self.cancelled,
            'approvedAt': self.approvedAt,
            'paymentIntent': self.paymentIntent,
            'deliveredWork': list(self.deliveredWork),
            'requestExtension': self.requestExtension.as_dict(),
            'dateOrdered': str(self.dateOrdered),
            'events': self.events.as_dict(),
            'buyerReview': self.buyerReview.as_dict(),
            'sellerReview': self.sellerReview.as_dict(),
        }
        return order
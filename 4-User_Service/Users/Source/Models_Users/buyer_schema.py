from mongoengine import Document, BooleanField, StringField, ListField, DateTimeField, ReferenceField 
class Buyer(Document):
    username = StringField(required=True, index=True)
    email = StringField(required=True, index=True)
    profile_pic = StringField(required=True)
    country = StringField(required=True)
    is_seller = BooleanField(default=False)
    purchased_gigs = ListField(ReferenceField('Gig'))
    created_at = DateTimeField()




from mongoengine import Document, StringField, ListField, FloatField, IntField, BooleanField

class Gig(Document):
    sellerId = StringField(required=True, error_messages={
        'required': 'Seller Id is required',
        'string': 'Seller Id must be of type string'
    })
    username = StringField(required=True, error_messages={
        'required': 'username is required',
        'string': 'username must be of type string'
    })
    email = StringField(required=True, error_messages={
        'required': 'email is required',
        'string': 'email must be of type string'
    })
    profilePicture = StringField(required=True, error_messages={
        'required': 'Profile picture is required',
        'string': 'Please add a profile picture'
    })
    title = StringField(required=True, error_messages={
        'required': 'Gig title is required',
        'string': 'Please add a gig title'
    })
    description = StringField(required=True, error_messages={
        'required': 'Gig description is required',
        'string': 'Please add a gig description'
    })
    categories = StringField(required=True, error_messages={
        'required': 'Gig category is required',
        'string': 'Please select a category'
    })
    subCategories = ListField(StringField(), required=True, min_size=1, error_messages={
        'required': 'Gig subcategories are required',
        'string': 'Please add at least one subcategory',
        'min_size': 'Please add at least one subcategory'
    })
    tag = ListField(StringField(), required=True, min_size=1, error_messages={
        'required': 'Gig tags are required',
        'string': 'Please add at least one tag',
        'min_size': 'Please add at least one tag'
    })
    price = FloatField(required=True, min_value=5.0, error_messages={
        'required': 'Gig price is required',
        'string': 'Please add a gig price',
        'min_value': 'Gig price must be greater than $4.99'
    })
    coverImage = StringField(required=True, error_messages={
        'required': 'Gig cover image is required',
        'string': 'Please add a cover image'
    })
    expectedDelivery = StringField(required=True, error_messages={
        'required': 'Gig expected delivery is required',
        'string': 'Please add expected delivery'
    })
    basicTitle = StringField(required=True, error_messages={
        'required': 'Gig basic title is required',
        'string': 'Please add basic title'
    })
    basicDescription = StringField(required=True, error_messages={
        'required': 'Gig basic description is required',
        'string': 'Please add basic description'
    })
    active = BooleanField(required=True, error_messages={
        'required': 'Gig Status is required',
        'string': 'Please add Active Status'
    })
    sortId = IntField(required=True, error_messages={
        'required': 'Sort Id is required',
        'string': 'Sort Id must be of type string'
    })


    def as_dict(self):
        gig_dict = {
            'sellerId': self.sellerId,
            'username': self.username,
            'email': self.email,
            'profilePicture': self.profilePicture,
            'title': self.title,
            'description': self.description,
            'categories': self.categories,
            'subCategories': self.subCategories,
            'tag': self.tag,
            'price': self.price,
            'coverImane': self.coverImage,
            'expectedDelivery':self.expectedDelivery,
            'basicTitle': self.basicTitle,
            'basicDescription': self.basicDescription,
            'sortId': self.sortId,
            'active': self.active
        }
        return gig_dict
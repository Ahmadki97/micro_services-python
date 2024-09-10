import mongoengine as db
from mongoengine import ValidationError, Document, EmbeddedDocument, StringField, BooleanField, IntField, ListField, DateTimeField, EmbeddedDocumentField, URLField
import datetime


class Language(EmbeddedDocument):
    language = StringField(required=True)
    level = StringField(required=True)


    def as_dict(self):
        language = {
            'language': self.language,
            'level': self.level
        }


class Experience(EmbeddedDocument):
    company = StringField(default='')
    title = StringField(default='')
    start_date = StringField(default='')
    end_date = StringField(default='')
    description = StringField(default='')
    currently_working_here = BooleanField(default=False)

    def as_dict(self):
        experience = {
            'company': self.company,
            'title': self.title,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'description': self.description,
            'currently_working_here': self.currently_working_here
        }
        return experience


class Education(EmbeddedDocument):
    country = StringField(default='')
    university = StringField(default='')
    title = StringField(default='')
    major = StringField(default='')
    year = StringField(default='')


    def as_dict(self):
        education = {
            'country': self.country,
            'university': self.university,
            'title': self.title,
            'major': self.major,
            'year': self.year
        }
        return education

class Certificate(EmbeddedDocument):
    name = StringField()
    from_ = StringField(db_field='from')
    year = IntField()


    def as_dict(self):
        certificate = {
            "name": self.name,
            "from_": self.from_,
            "year": self.year
        }
        return certificate


class RatingCategory(EmbeddedDocument):
    value = IntField()
    count = IntField()




class Seller(Document):
    fullname = StringField(required=True)
    username = StringField(required=True, index=True, unique=True)
    email = StringField(required=True, unique=True)
    profile_pic = StringField(required=True)
    description = StringField(required=True)
    profile_public_id = StringField(required=True)
    oneliner = StringField(required=True,default='')
    country = StringField(required=True)
    languages = ListField(EmbeddedDocumentField(Language))
    skills = ListField(StringField(required=True))
    rating_count = IntField(default=0)
    rating_sum = IntField(default=0)
    rating_categories = {
        'five': EmbeddedDocumentField(RatingCategory),
        'four': EmbeddedDocumentField(RatingCategory),
        'three': EmbeddedDocumentField(RatingCategory),
        'two': EmbeddedDocumentField(RatingCategory),
        'one': EmbeddedDocumentField(RatingCategory),
    }
    response_time = IntField(default=0)
    recent_delivery = DateTimeField()
    experience = ListField(EmbeddedDocumentField(Experience))
    education = ListField(EmbeddedDocumentField(Education))
    social_links = ListField(URLField())
    certificates = ListField(EmbeddedDocumentField(Certificate))
    ongoing_jobs = IntField(default=0)
    completed_jobs = IntField(default=0)
    cancelled_jobs = IntField(default=0)
    total_earnings = IntField(default=0)
    total_gigs = IntField(default=0)
    created_at = DateTimeField(default=datetime.datetime.now)

    meta = {'collection': 'sellers', 'indexes': ['username', 'email'], 'strict': False}


    def clean(self):
        if not self.languages or len(self.languages)==0:
            raise ValidationError('At least one language is required')
        if not self.skills or len(self.skills)==0:
            raise ValidationError('At least one skill is required')
        if self.response_time <= 0:
            raise ValidationError('responseTime must be greater than zero')
        if not self.experience or len(self.experience) == 0:
            raise ValidationError('At least one experience is required')
        if not self.education or len(self.education) == 0:
            raise ValidationError('At least one education is required')
        
        
    def as_dict(self):
        certificates = [cert.as_dict() for cert in self.certificates]
        education = [educate.as_dict() for educate in self.education]
        languages = [language.as_dict() for language in self.languages]
        experience = [experience.as_dict() for experience in self.experience]
        seller = {
            'fullname': self.fullname,
            'username': self.username,
            'email': self.email,
            'profile_pic': self.profile_pic,
            'description': self.description,
            'profile_public_id': self.profile_public_id,
            'oneliner': self.oneliner,
            'country': self.country,
            'languages': languages,
            'skills': self.skills,
            'rating_count': self.rating_count,
            'rating_sum': self.rating_sum,
            # 'rating_categories': dict(str(self.rating_categories)),
            'response_time': self.response_time,
            'recent_delivery': self.recent_delivery,
            'experience': experience,
            'education': education,
            'social_links': self.social_links,
            'certificates': certificates,
            'ongoing_jobs': self.ongoing_jobs,
            'completed_jobs': self.completed_jobs,
            'cancelled_jobs': self.cancelled_jobs,
            'total_earnings': self.total_earnings,
            'total_gigs': self.total_gigs,
            'created_at': str(self.created_at)
        }
        return seller



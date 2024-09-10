from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired, Email, URL, NumberRange

class LanguageForm(FlaskForm):
    language = StringField('Language', validators=[DataRequired()])
    level = StringField('Level', validators=[DataRequired()])

class ExperienceForm(FlaskForm):
    company = StringField('Company', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    start_date = StringField('Start Date', validators=[DataRequired()])
    end_date = StringField('End Date', validators=[DataRequired()])
    description = StringField('Description')
    currently_working_here = StringField('Currently Working Here')

class EducationForm(FlaskForm):
    country = StringField('Country', validators=[DataRequired()])
    university = StringField('University', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])

class CertificateForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    from_ = StringField('From', validators=[DataRequired()])
    year = IntegerField('Year', validators=[NumberRange(min=1900, max=2100)])

class SellerForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_pic = StringField('Profile Picture', validators=[DataRequired(), URL()])
    description = StringField('Description', validators=[DataRequired()])
    profile_public_id = StringField('Profile Public ID', validators=[DataRequired()])
    oneliner = StringField('One-liner')
    country = StringField('Country', validators=[DataRequired()])
    languages = FieldList(FormField(LanguageForm), min_entries=1)
    skills = FieldList(StringField('Skill', validators=[DataRequired()]), min_entries=1)
    response_time = IntegerField('Response Time', validators=[NumberRange(min=1)])
    recent_delivery = DateField('Recent Delivery')
    experience = FieldList(FormField(ExperienceForm), min_entries=1)
    education = FieldList(FormField(EducationForm), min_entries=1)
    social_links = FieldList(StringField('Social Link', validators=[URL()]))
    certificates = FieldList(FormField(CertificateForm))
    submit = SubmitField('Create Seller')
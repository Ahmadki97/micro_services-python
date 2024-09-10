from flask import jsonify, request, Blueprint
from faker import Faker
from http import HTTPStatus
from Services.seller_service import createSeller, getSellerByEmail
from Services.buyer_services import getRandomBuyers
from Helper_Users.verify_token import jwt_required
from Helper_Users.errorhandlers import BadRequestError
import random
import uuid


seller_seed_blueprint = Blueprint('seller_Seed', __name__, url_prefix='/api/v1/users/sellers')

@seller_seed_blueprint.route('/seed-sellers/<int:count>', methods=['PUT'])
@jwt_required
def seed(count):
    faker = Faker()
    buyers = getRandomBuyers(count) 
    for buyer in buyers:
        seller = getSellerByEmail(buyer['email'])
        if seller is not None:
            raise BadRequestError("Seller Already Exists", "SellerSeed() Method Error")
        else:
            basic_description = faker.sentence(nb_words=20)
            skills = ['Programming', 'Web Development', 'Mobile Application', 'Proof reading', 'UI/UX', 'Data Science', 'Financial modeling', 'Data analysis']
            seller_data = {
                'profile_public_id':str(uuid.uuid4()),
                'fullname': faker.name(),
                'username': buyer['username'],
                'email': buyer['email'],
                'profile_pic': buyer['profile_pic'],
                'description': basic_description,
                'oneliner': ' '.join(Faker().words(nb=random.randint(5, 10))), 
                'country': faker.country(),
                'skills': random.sample(skills, random.randint(1, 4)),
                'languages': [
                    {'language': 'English', 'level': 'Native'},
                    {'language': 'Spanish', 'level': 'Basic'},
                    {'language': 'German', 'level': 'Basic'}
                ],
                'response_time': random.randint(1, 5), 
                'experience': randomExperience(random.randint(2, 4)),
                'education': randomEducation(random.randint(2, 4)),
                'social_links': ['https://kickchatapp.com', 'http://youtube.com', 'https://facebook.com'],
                'certificates':[
                    {
                        'name': 'Flutter App Developer',
                        'from': 'Flutter Academy',
                        'year': 2021
                    },
                    {
                        'name': 'Android App Developer',
                        'from': '2019',
                        'year': 2020
                    },
                    {
                        'name': 'IOS App Developer',
                        'from': 'Apple Inc.',
                        'year': 2019
                    }
                ]
            } 
            print('Seller Data is : ', seller_data)
            createSeller(seller_data)
        response = {
            'Message': "Sellers Created Successfully",
            'HTTP_Status': HTTPStatus.OK
        }
        return jsonify(response)
    


def randomExperience(count):
    fake = Faker()
    result =[]
    for x in range(count-1):
        random_start_year = [2020, 2021, 2022, 2023, 2024, 2025]
        random_end_year = ['Present', 2024, 2025, 2026, 2027]
        end_year = random.choice(random_end_year)
        experience = {
            'company': fake.company(),
            'title': fake.job(),
            'start_date': f"{fake.month()} {random.choice(random_start_year)}",
            'end_date': 'Present' if end_year == 'Present' else f"{fake.month()} {end_year}",
            'description': fake.sentence(nb_words=100),
            'currently_working_here': end_year == 'Present'
        }
        result.append(experience)
    return result



def randomEducation(count):
    fake = Faker()
    result = []
    for x in range(count-1):
        random_year = [2020, 2021, 2022, 2023, 2024, 2025]
        education = {
            'country': fake.country(),
            'university': fake.job(),
            'title': fake.job(),
            'major': fake.company_suffix(),
            'year': str(random.choice(random_year)) 
        }
    result.append(education)
    return result



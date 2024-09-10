from Helper_Gig.elastic import elastic_connection
from Services_GIg.search_service import gigsSearch
from Queues_Gig.gig_producer import startPublishGigs
from Models_Gig.gig_schema import Gig
from Helper_Gig.logHandler import logger
from faker import Faker
import json
import random

def getGigId(id: str):
    gig = elastic_connection.getDocumentById(index_name='gigs', document_id=id)
    return gig


def getSellerGigs(seller_id: str):
    gigs = gigsSearch(seller_id, True)
    return gigs


def getSellerPausedGigs(seller_id: str):
    gigs = gigsSearch(seller_id, False)


def createGig(data: dict):
    # First We Create the Gig in The MongoDB
    try:
        gig = Gig(**data)
        print('Gig is ', gig)
        gig.save()
        print('Gig Saved to DB')
        body = {
            'seller_id': gig['sellerId'],
            'count': 1,
            'type': 'update-gig-count',
        }
        print('Body is :', body)
        # Then We Send a message to the USers Service to to update the Gigs Count that a Seller has  
        startPublishGigs(exchange_name='', routing_key='order-seller', body=body)
        logger.info("createGig() Method, Sending a Message to the User Service..")
        # Then we add the Gig Document to the Elasticsearch 
        elastic_connection.addDocument(index_name='gigs', document_id=gig.id, document=gig.as_dict())
        return gig
    except Exception as err:
        logger.error(f"Error in createGig() Method : {str(err)}")
    

def deleteGig(gig_id: str, seller_id: str):
    try:
        gig = Gig.objects.get(id=gig_id)
        print('gig is :', gig)
        print('gig id in service is :', gig_id)
        gig.delete()
        logger.info(f"deleteGig() Method, Gig Deleted from MongoDB")
        body = {
            'seller_id': seller_id,
            'count': -1,
            'type': 'update-gig-count',
        }
        startPublishGigs('', 'order-seller', json.dumps(body))
        logger.info("deleteGig() Method, Sending a Message to the User Service..")
        elastic_connection.deleteDocument(index_name='gigs', document_id=gig_id)
        return True
    except Exception as err:
        logger.error(f"Error in deleteGig() Method: {str(err)}")
        return False
    
    
def updateGig(gig_id: str, gig_data: dict):
    try:
        gig = Gig.objects.get(id=gig_id)
        print('Gig is :', gig)
        gig.modify(**gig_data)
        logger.info(f"updateGig() Method, Gig with id {gig_id} Updated Successfully.")
        elastic_connection.updateDocument(index_name='gigs', document_id=gig.id, document=gig.as_dict())
        return gig.as_dict()
    except Exception as err:
        logger.error(f"Error in updateGig() Method : {str(err)}")
        return("Could Not Update Gig")


def updateActiveGig(gig_id: str, active: bool):
    try:
        gig = Gig.objects.get(id=gig_id)
        gig.modify(active=active)
        gig.save()
        logger.info(f"updateActiveGig() Method, Gig with id {gig_id} Updated Successfully.")
        elastic_connection.updateDocument(index_name='gigs', document_id=gig_id, document=gig.as_dict())
        return gig
    except Exception as err:
        logger.error(f"Error in updateActiveGig() Method : {str(err)}")
        return False


def updateGigReview(data:dict):
    try:
        gig_id = data['gig_id']
        rating = data['rating']
        rating_types = {
            '1': 'one',
            '2': 'two',
            '3': 'three',
            '4': 'four',
            '5': 'five',
        }
        rating_key = rating_types[str(rating)]
        gig = Gig.objects(id=gig_id).first()
        if gig :
            gig.ratings_count += 1
            gig.rating_sum += rating
            gig.rating_categories.setdefault(rating_key, {'value': 0, 'count': 0})
            gig.rating_categories[rating_key]['value'] += rating
            gig.rating_Categories[rating_key]['count'] += 1
            gig.save()       
            logger.info("updateGigReview() Method, Gig Review Updated Successfully")
    except Exception as err:
        logger.error(f"Error in updateGigReview() Method : {str(err)}")
        return(json.load('Gig Could not be updated'))
    

def seedData(sellers: list, count: int):
    try:
        CATEGORIES = (
            'Graphics & Design',
            'Digital Marketing',
            'Writing & Translation',
            'Video & Animation',
            'Music & Audio',
            'Programming & Tech',
            'Data',
            'Business'
        )
        EXPECTED_DELIVERY = (
            '1 Day Delivery',
            '2 Days Delivery',
            '3 Days Delivery',
            '4 Days Delivery',
            '5 Days Delivery',
        )
        RANDOM_RATINGS = [
            {'sum': 20, 'count': 4},
            {'sum': 10, 'count': 2},
            {'sum': 20, 'count': 4},
            {'sum': 15, 'count': 3},
            {'sum': 5, 'count': 1},
        ]
        faker = Faker()   
        for seller in sellers:
            title = f"I Will {faker.words(5)}"
            basicTitle = faker.sentence(nb_words=3)
            basic_description = faker.sentence(nb_words=10)
            gig = {
                'profilePicture': seller.get('profile_pic'),
                'sellerId': seller.get('_id'),
                'email': seller.get('email'),
                'username': seller.get('username'),
                'title': title,
                'basicTitle': basicTitle,
                'basicDescription': basic_description,
                'categories': random.choice(CATEGORIES),
                'subCategories': list(faker.sentence(nb_words=2)),
                'description': faker.sentence(nb_words=20),
                'tag': list(faker.sentence(nb_words=2)),
                'price': faker.pyfloat(min_value=0.01, max_value=100.00, right_digits=2),
                'coverImage': faker.image_url(),
                'expectedDelivery': random.choice(EXPECTED_DELIVERY),
                'sortId': faker.pyint(min_value=1, max_value=20),
            }
            createGig(gig)
        logger.info(f"Gig {gig} Created Successfully.")
    except Exception as err:
        logger.error(f"Error in seedData() Method : {str(err)}")
        
        
         


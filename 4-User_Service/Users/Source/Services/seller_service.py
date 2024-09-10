from Models_Users.seller_schema import Seller
from Services.buyer_services import updateBuyerIsSeller
from Helper_Users.logHandler import logger

def getSellerById(id: str):
    try:
        print("Hello from Sellers Services")
        seller = Seller.objects.get(id=id)
        return seller
    except Exception as err:
        logger.error(f"error in getSellerById() Method : {str(err)}")


def getSellerByusername(username:str):
    seller = Seller.objects.get(username=username)
    return seller


def getSellerByEmail(email:str):
    seller = Seller.objects(email=email).first()
    return seller


def getRandomSellers(count:int):
    sellers = Seller.objects.sample(count)
    return sellers


def createSeller(seller_data):
    seller = Seller(**seller_data)
    seller.save()
    # updateBuyerIsSeller(seller.email)
    return seller


def updateSeller(seller_id: str, seller_data: dict):
    updated_seller = Seller.objects.get(id=seller_id)
    updated_seller.modify(**seller_data)
    updated_seller.save()
    print('Updated Seller fullname is :', updated_seller.fullname)
    return updated_seller


def updateTotalGigsCount(seller_id: str, count: int):
    seller = Seller.objects(id=seller_id).first()
    seller.total_gigs += count


def updateOngoingJobs(seller_id: str, ongoing_jobs: int):
    seller = Seller(id=seller_id).first()
    seller.ongoing_jobs += ongoing_jobs
    seller.save()


def updateSellerCanceledJobs(selelr_id):
    seller = Seller.objects(id=selelr_id).first()
    seller.ongoing_jobs -= 1
    seller.canceled_jobs += 1
    seller.save()


def updateSellerCompletedJobs(data:dict):
    selelr_id = data['seller_id']
    seller = Seller.objects(id=selelr_id).first()
    if seller:
        seller.ongoing_jobs += data['ongoing_jobs']
        seller.completed_jobs += data['completed_jobs']
        seller.total_earnings += data['total_earnings']
        seller.recent_delivery += data['recent_delivery']
        seller.save()


def updateSellerReview(data:dict):
    seller_id = data['seller_id']
    rating = data['rating']
    rating_types = {
        '1': 'one',
        '2': 'two',
        '3': 'three',
        '4': 'four',
        '5': 'five',
    }
    rating_key = rating_types[str(rating)]
    seller = Seller.objects(id=seller_id).first()
    if seller :
        seller.ratings_count += 1
        seller.rating_sum += rating
        seller.rating_categories.setdefault(rating_key, {'value': 0, 'count': 0})
        seller.rating_categories[rating_key]['value'] += rating
        seller.rating_Categories[rating_key]['count'] += 1
        seller.save()
        
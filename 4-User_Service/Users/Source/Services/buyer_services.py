from flask import jsonify
from Models_Users.buyer_schema import Buyer


def getBuyerByEmail(email):
    buyer = Buyer.objects(email=email).first()
    return buyer


def getBuyerByUsername(username):
    buyer = Buyer.objects(username=username).first()
    return buyer


def getRandomBuyers(count):
    pipeline = [
      {"$sample": {"size": count}}  # Sample 'count' documents
  ]
    buyers = Buyer.objects.aggregate(*pipeline)  # Perform aggregation
    return buyers



def createBuyer(buyer_data):
    email = buyer_data['email']
    existing_buyer = getBuyerByEmail(email)
    if existing_buyer:
        return jsonify({'message': 'Buyer already exists..'})
    else:
        buyer = Buyer(**buyer_data)
        buyer.save()
        return jsonify({'message': 'Buyer is Created..'})
    

def updateBuyerIsSeller(email):
    buyer = getBuyerByEmail(email)
    buyer.is_seller = True
    buyer.save()


def updateBuyerPurchasedGigs(buyer_id, purchased_gig_id, type):
    buyer = Buyer(id=id)
    if type == 'purchased-gigs':
        buyer.purchased_gigs.append(purchased_gig_id)
        buyer.save()
    else:
        buyer.purchased_gigs.remove(purchased_gig_id)
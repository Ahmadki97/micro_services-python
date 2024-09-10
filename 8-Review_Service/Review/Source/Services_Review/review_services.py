from Helper_Review.logHandler import logger
from Models_Review.database import db, Review
from Queues_Review.review_producer import startPublish
import json


def addReview(data: dict):
    try:
        review = Review(**data)
        print(f"DB Session is {db.session.info}")
        db.session.rollback()
        db.session.add(review)
        db.session.commit()
        print(f"Review is {review}")
        logger.info(f"addReview() Method, new review with id {review.id} created successfully.")
        message_details = {
            "gigId": review.gigid,
            "reviewerId": review.reviewerid,
            "sellerId": review.sellerid,
            "review": review.review,
            "rating": review.rating,
            "orderId": review.orderid,
            "createdAt": review.createdat
        }
        startPublish(exchange_name='review-user-exchange', routing_key='review-user', service_name='User', body=json.dumps(message_details, default=str))
        return review    
    except Exception as err:
        logger.error(f"Error in addReview() Method: {str(err)}")


def getReviewsByGigId(gig_id: str):
    try:
        reviews = db.session.query(Review).filter(Review.gigid==gig_id)
        logger.info(f"getReviewsByGigId() Method, Reviews with gigId {gig_id} Found Successfully.")
        reviews_list = []
        for review in reviews:
            reviews_list.append(review)
        return reviews_list
    except Exception as err:
        logger.error(f"Error in getReviewsByGigId() Method: {str(err)}")


def getReviewsBySellerId(seller_id: str):
    try:
        reviews = db.session.query(Review).filter(Review.sellerid==seller_id)
        logger.info(f"getReviewsByGigId() Method, Reviews with sellerId {seller_id} Found Successfully.")
        reviews_list = []
        for review in reviews:
            reviews_list.append(review)
        return reviews_list
    except Exception as err:
        logger.error(f"Error in getReviewsBySellerId() Method: {str(err)}")
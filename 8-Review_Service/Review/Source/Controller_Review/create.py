from Helper_Review.logHandler import logger
from Services_Review.review_services import addReview
from Helper_Review.verify_token import jwt_required
from flask import request, Blueprint
from http import HTTPStatus
import datetime
import json


create_blueprint = Blueprint('Create_Blueprint', __name__, url_prefix='/api/v1/review')


@create_blueprint.route('/', methods=['POST'])
@jwt_required
def createReview():
    try:
        data = request.get_json()
        print(f"gigId is {data['gigId']}")
        order_data = {
            "gigid": data['gigId'],
            "reviewerid": data['reviewerId'],
            "orderid": data['orderId'],
            "sellerid": data['sellerId'],
            "reviewerimage": data['reviewerImage'],
            "review": data['review'],
            "reviewtype": data['reviewType'],
            "reviewerusername": data['reviewerUsername'],
            "country": data['country'],
            "createdat": datetime.datetime.now(),
            "rating": data['rating'], 
        }
        print(f"Order data is {order_data}")
        review = addReview(data=order_data)
        logger.info(f"create review controller, new review with id {review.id} created successfully")
        response = {
            "Message": "Review created successfully",
            "Http Status": HTTPStatus.OK,
            "Review": review
        }
        return(json.dumps(response, default=str))
    except Exception as err:
        logger.error(f"Error in createReview Controller: {str(err)}")
        return(f"Could not create review: please try again later")
    
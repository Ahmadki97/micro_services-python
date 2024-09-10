from http import HTTPStatus
from flask import jsonify, Blueprint


health_route = Blueprint('API_Service_Health_Route', __name__)


@health_route.route('/health', methods=['GET'])
def authHealth():
    response = {
        'message': 'Authentication Service is up and running..',
        'HTTP_STATUS': HTTPStatus.OK,
    }
    return jsonify(response)
from http import HTTPStatus
from flask import jsonify, Blueprint


health_route = Blueprint('Chat_Service_Health_Route', __name__, url_prefix='/api/v1/chat')


@health_route.route('/health', methods=['GET'])
def authHealth():
    response = {
        'message': 'Chat Service is up and running..',
        'HTTP_STATUS': HTTPStatus.OK,
    }
    return jsonify(response)
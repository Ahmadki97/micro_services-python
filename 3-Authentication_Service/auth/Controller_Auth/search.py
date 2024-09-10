from Services_Auth.search_service import * 
from flask import request, jsonify, Blueprint
from Helper_Auth.verify_token import jwt_required
from http import HTTPStatus


search_route = Blueprint('Search', __name__, url_prefix='/api/v1/auth')


@search_route.route('/search-gig', methods=['GET'])
@jwt_required
def gitGigs():
    size = request.args['size']
    from_value = request.args['from']
    type_value = request.args['type'] 
    result_hits = []
    paginate = {
        'size': size,
        'from': from_value,
        'type_value': type_value
    }
    gigs = gigsSearch(search_query=request.query_string,
                       paginate=paginate, 
                       delivery_time=request.args.get('delivery_time'),
                       min= int(request.args.get('min')),
                       max= int(request.args.get('max'))
                       )
    for item in gigs['hits']:
        result_hits.append(item._source)
    
    if type == 'backward':
        result_hits = sorted(result_hits, key=lambda x: x['sortId'], reverse=True)

    result = {
        'message': 'Search Gigs Result Is :',
        'TOTAL': gigs['total'],
        'HITS': gigs['hits'],
        'RESULT_HITS': result_hits,
        'HTTP_STATUS': HTTPStatus.OK
    }

    return jsonify(result)
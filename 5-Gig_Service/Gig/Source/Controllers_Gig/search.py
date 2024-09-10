from flask import request, jsonify, Blueprint
from Services_GIg.search_service import gigsSearch, gigsSearchAll
from Helper_Gig.verify_token import jwt_required
from http import HTTPStatus



gigsearch_blueprint = Blueprint('Search_Gig', __name__, url_prefix='/api/v1/gig')



@gigsearch_blueprint.route('/gig-search', methods=['GET'])
@jwt_required
def getGigs():
    size = request.args['size']
    from_value = request.args['from']
    type_value = request.args['type'] 
    result_hits = []
    paginate = {
        'size': size,
        'from': from_value,
        'type_value': type_value
    }
    gigs = gigsSearchAll(search_query=request.query_string,
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
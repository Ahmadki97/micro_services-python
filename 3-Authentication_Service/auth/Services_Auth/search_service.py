from Helper_Auth.elastic import elastic_connection

def gigById(index_name, document_id):
    gig = elastic_connection.getDocumentById(index_name, document_id)
    return gig


def gigsSearch(search_query, paginate, delivery_time, min, max):
    from_value = paginate['from']
    size_value = paginate['size']
    type_value = paginate['type']
    query_list = [
        {
            'query_string': {
                'fields': ['username', 'title', 'description', 'basicDescription', 'basicTitle', 'categories', 'subCategories', 'tags'],
                'query': f"{search_query}"
                }
        },
        {
            'term': {
                'active': True,
            }
        }
    ]

    if delivery_time is not None:
        query_list.append({
            'query_string': {
                'fields': ['expectedDelivery'],
                'query': f"*{delivery_time}*"
            }
        })

    if min is not None and max is not None:
        query_list.append({
            'range': {
                'gte': min,
                'lte': max
            }
        })

    search_response = elastic_connection.client.search(
        index='gigs',
        size=size_value,
        body={
            'query':{
                'bool': {
                    'must': query_list
                }
            },
            'sort': [
                {
                    'sortId': 'asc' if type_value == 'forwards' else 'desc'
                }
            ],
            **({'search_after':[from_value]} if from_value !=0 else {})
        }
    )

    total = search_response['hits']['total']['value']
    hits = search_response['hits']['hits']

    return {
        'total':total,
        'hits':hits
    }
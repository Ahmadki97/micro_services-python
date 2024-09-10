from Helper_Gig.elastic import elastic_connection



def gigsSearch(seller_id: str, active: bool):
    query = {
        "bool": {
            "must": [
                {"match": {"sellerId": seller_id}},
                {"match": {"active": active}}
            ]
        }
    }
    response = elastic_connection.client.search(index='gigs', query=query)
    documents = [doc['_source'] for doc in response["hits"]["hits"] if '_source' in doc]
    return documents


def gigsSearchAll(search_query, paginate, delivery_time, min, max):
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


def gigsSearchByCategory(search_query):
    query_list = [
        {
            'query_string': {
                'fields': ['categories'],
                'query': f"{search_query}"
                }
        },
        {
            'term': {
                'active': True,
            }
        }
    ]
    search_response = elastic_connection.client.search(
        index='gigs',
        size=10,
        body={
            'query':{
                'bool': {
                    'must': query_list
                }
            }
        }
    )

    total = search_response['hits']['total']['value']
    hits = search_response['hits']['hits']

    return {
        'total':total,
        'hits':hits
    }


def getMoreGigsLikeThis(gig_id: str):
    query_body = {
        "query": {
            "more_like_this": {
                "fields": [
                    "username", "title", "description", "basicDescription",
                    "basicTitle", "categories", "subCategories", "tags"
                ],
                "like": [
                    {
                        "_index": "gigs",
                        "_id":gig_id
                    }
                ]
            }
        }
    }
    result = elastic_connection.client.search(index='gigs', size= 5, body=query_body)
    print('Result is :', result)
    return result


def getTopRatedGIgByCategory(category_filter: str):
    threshold = 5
    query_body = {
        "bool": {
            "must": [
                {
                    "script": {
                        "script": {
                            "source": "doc['ratingSum'].value != 0 && (doc['ratingSum'].value / doc['ratingCount'].value >= params['threshold'])",
                            "lang": "painless",
                            "params": {
                                "threshold": threshold
                            }
                        }
                    }
                },
                {
                    "query_string": {
                        "fields": ["categories"],
                        "query": category_filter
                    }
                }
            ]
        }
    }
    result = elastic_connection.client.search(index='gigs', size=10, body=query_body)
    return result

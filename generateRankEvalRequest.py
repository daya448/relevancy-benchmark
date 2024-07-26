import json
import sys
import math
from es_client import get_elasticsearch_client,read_config

es = get_elasticsearch_client()
config = read_config('config.txt')

def printAllQueries():
    with open('discernatron_ratings.tsv', 'r') as f:
        querySet = set()
        for line in f:
            parts = line.split('\t')
            querySet.add(parts[0])
        print('To create a rank eval request, add the queries you want to include as parameters.')
        print('The following queries are available: \n')
        print("\n".join(str(e) for e in querySet))


def createRequestForQuery(queryString, requestId):
    with open('discernatron_ratings.tsv', 'r') as f:
        ratingDocTitlesAndRatings = set()
        for line in f:
            parts = line.split('\t')
            if (queryString == parts[0]):
                ratingDocTitlesAndRatings.add((parts[1], parts[2]))

    idsAndRatings = set()

    for docTitle in ratingDocTitlesAndRatings:
        query = {
            "query": {
                "match": {
                    "title.keyword": docTitle[0]
                }
            }
        }
        queryResult = es.search(body=query)
        try:
            docId = queryResult['hits']['hits'][0]['_id']
            idsAndRatings.add((docId, docTitle[1]))
            print( docTitle[0])
        except:
            print('Failed for title ' + docTitle[0])

    ratings = []
    for idAndRating in idsAndRatings:
        ratings.append(
            {
                '_index': 'enwiki_rank',
                '_id': str(idAndRating[0]),
                'rating': math.floor(float(idAndRating[1]))
            }
        )
    request = {
        'id': requestId,
        'template_id': 'templated_query',
        'ratings': ratings,
        "summary_fields": [
            "title"
        ],
        "params": {
            "query_string": queryString
        }
    }
    return request


def createRequestForQueries(queryStrings):
    requests = []
    for queryString in queryStrings:
        print('Processing query ' + queryString)
        requests.append(createRequestForQuery(
            queryString, queryString.replace(" ", "_") + "_query"))

    return {
        'requests': requests

    }


def main(argv):
    if len(argv) == 0:
        printAllQueries()
    else:
        request = createRequestForQueries(argv)
        output_file = 'rank_eval_request.json'
        with open(output_file, 'w') as f:
            json.dump(request, f, indent=4)
        print(f"Rank evaluation request saved to {output_file}.")


if __name__ == '__main__':
    main(sys.argv[1:])

# search_queries.py

def get_search_query(query_type, query_vector=None, query_string=None):
    if query_type == "base_query":
        return {
            "query": {
                "match": {
                    "text": query_string
                }
            }

        }
    elif query_type in ["vector_query"]:
        return {
            "knn": {
                "field": "emb",  # Use the passed field name
                "query_vector": query_vector,
                "k": 100,
                "num_candidates": 1000
            }
        }
    elif query_type in ["elser_query"]:
        return {
            "knn": {
                "field": "text_elser",  # Use the passed field name
                "query_vector": query_vector,
                "k": 100,
                "num_candidates": 1000
            }
        }
    elif query_type == "hybrid_query":
        return {
            "query": {
                "match": {
                    "text": query_string
                }
            },
            "knn": {
                "field": "emb",
                "query_vector": query_vector,
                "k": 10,
                "num_candidates": 100
            },
            "rank": {
                "rrf": {
                    "window_size": 10,
                    "rank_constant": 5
                }
            }
        }
    else:
        raise ValueError("Invalid query type specified.")

import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_search_query(query_type, query_vector=None, query_string=None):
    logging.debug(f"Generating search query for type: {query_type}")

    if query_type == "base_query":
        logging.debug(f"Query string: {query_string}")
        return {
            "query": {
                "match": {
                    "text": query_string
                }
            }
        }
    elif query_type == "vector_query":
        logging.debug(f"Query vector: {query_vector}")
        return {
            "knn": {
                "field": "emb",  # Use the passed field name
                "query_vector": query_vector,
                "k": 100,
                "num_candidates": 1000
            }
        }
    elif query_type == "elser_query":
        logging.debug(f"Query vector: {query_vector}")
        return {
            "query": {
                "text_expansion": {
                    "text_emb": {
                        "model_id": ".elser_model_2_linux-x86_64",
                        "model_text": {query_vector}
                    }
                }
            }
        }
    elif query_type == "hybrid_query":
        logging.debug(
            f"Query string: {query_string}, Query vector: {query_vector}")
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
        logging.error(f"Invalid query type specified: {query_type}")
        raise ValueError("Invalid query type specified.")

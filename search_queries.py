import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_search_query(query_type, query_vector=None, query_string=None, k=1):
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
                "k": k,
                "num_candidates": k*10
            }
        }
    elif query_type == "elser_query":
        logging.debug(f"Query vector: {query_vector}")
        return {
            "query": {
                "text_expansion": {
                    "text_emb": {
                        "model_id": ".elser_model_2_linux-x86_64",
                        "model_text": query_vector
                    }
                }
            }
        }
    elif query_type == "hybrid_query":
        logging.debug(
            f"Query string: {query_string}, Query vector: {query_vector}")
        return {
            "query": {
                "multi_match": {
                    "query":  query_string,
                    "fields": ["full_text.english"],
                    "type": "most_fields"  
                }          
            },
            "knn": {
                "field": "emb",
                "query_vector": query_vector,
                "k": k,
                "num_candidates": k*10
            },
            "rank": {
                "rrf": {
                    "window_size": k,
                    "rank_constant": 60
                }
            }
        }
    elif query_type == "hybrid_query_linear":
        logging.debug(
            f"Query string: {query_string}, Query vector: {query_vector}")
        return {
            "query": {
                "multi_match": {
                    "query":  query_string,
                    "fields": ["full_text.english"]  
                }          
            },
            "knn": {
                "field": "emb",
                "boost": 25,
                "query_vector": query_vector,
                "k": k,
                "num_candidates": k*10
            }
        }
    elif query_type == "bm25_english_text":
        logging.debug(f"Query string: {query_string}")
        return {
            "query": {
                "match": {
                    "text.english": query_string
                }
            }
        }
    elif query_type == "bm25_english_text":
        logging.debug(f"Query string: {query_string}")
        return {
            "query": {
                "match": {
                    "text.english": query_string
                }
            }
        }
    elif query_type == "bm25_english_full_text":
        logging.debug(f"Query string: {query_string}")
        return {
            "query": {
                "combined_fields": {
                    "query": query_string,
                    "fields": ["full_text.english"]
                }
            }
        }
    elif query_type == "bm25_english_text_title_plus_nostem":
        logging.debug(f"Query string: {query_string}")
        return {
            "query": {
                "multi_match": {
                    "query": query_string,
                    "fields": ["full_text.english", "full_text.english_nostem"],
                    "type": "best_fields"
                }
            }
        }
    elif query_type == "bm25_english_text_title_plus_nostem_cross":
        logging.debug(f"Query string: {query_string}")
        return {
            "query": {
                "multi_match": {
                    "query": query_string,
                    "fields": ["full_text.english", "full_text.english_nostem"],
                    "type": "cross_field"
                }
            }
        }
    elif query_type == "bm25_full_text_plus_nostem":
        logging.debug(f"Query string: {query_string}")
        return {
            "query": {
                "bool": {
                "must": [
                    {
                    "multi_match": {
                        "query": query_string,
                        "fields": [
                        "full_text.english"
                        ]
                    }
                    }
                ], 
                "should": [
                    {
                    "multi_match": {
                        "query": query_string,
                        "fields": [
                        "full_text.english_nostem"
                        ],
                        "type": "cross_fields"
                    }
                    }
                ]
                }
            }
        }
    else:
        logging.error(f"Invalid query type specified: {query_type}")
        raise ValueError("Invalid query type specified.")

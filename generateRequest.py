import json
import csv
from es_client import read_config

config = read_config('config.txt')


k = config['k']
relevant_rating_threshold = config['relevant_rating_threshold']
index_name = config['index_name']
benchmark_output_file = config['benchmark_output_file']

# Function to load JSON objects from a file where each JSON object is on a new line
def load_json_objects(filename):
    json_objects = []
    with open(filename, 'r') as file:
        content = file.read()
        objects = content.split('}\n{')
        for obj in objects:
            obj = obj.strip()
            if obj:
                if not obj.startswith('{'):
                    obj = '{' + obj
                if not obj.endswith('}'):
                    obj = obj + '}'
                try:
                    json_objects.append(json.loads(obj))
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {obj}")
                    print(f"Error message: {e}")
    return json_objects

# Load the queries
queries = load_json_objects('queries.json')

# Load the qrels from the qrels.tsv file
qrels = {}
with open('qrels.tsv') as f:
    headers = f.readline().strip().split()  # Read and split the header line
    for line in f:
        row = line.strip().split()
        query_id, doc_id, rating, ignore_field = row
        if query_id not in qrels:
            qrels[query_id] = []
        qrels[query_id].append({
            "_index": "your_index_name",  # Adjust this if you have a different index name
            "_id": doc_id,
            "rating": int(rating)
        })

rank_eval_requests = {
    "requests": [],
    "metric": {
        "recall": {
            "k": 10,
            "relevant_rating_threshold": 2
        }
    },
    "templates": [
        {
            "id": "templated_query",
            "template": {
                "inline": {
                    "query": {
                        "knn": {
                            "field": "emb",
                            "query_vector": "{{#toJson emb}}",
                            "k": 100,
                            "num_candidates": 1000
                        }
                    }
                }
            }
        }
    ]
}




# Define the inline templates for vector, hybrid, and elser queries
base_query_template = {
    "id": "templated_query",
    "template": {
        "inline": {
            "query": {
                "match": {
                    "text": "{{query_string}}"
                }
            }

        }
    }
}

vector_query_template = {
    "id": "templated_query",
    "template": {
        "inline": {
            "query": {
                "knn": {
                    "field": "emb",
                    "query_vector": "{{emb}}",
                    "k": "100",
                    "num_candidates": "1000"
                }
            }
        }
    }
}

hybrid_query_template = {
    "id": "templated_query",
    "template": {
        "inline": {
            "query": {
                "bool": {
                    "should": [
                        {
                            "knn": {
                                "field": "emb",
                                "query_vector": "{{emb}}",
                                "k": "100",
                                "num_candidates": "1000"
                            }
                        },
                        {
                            "match": {
                                "text": "{{query_string}}"
                            }
                        }
                    ]
                }
            }
        }
    }
}

elser_query_template = {
    "id": "templated_query",
    "template": {
        "inline": {
            "query": {
                "knn": {
                    "field": "text_elser",
                    "query_vector": "{{text_elser}}",
                    "k": "100",
                    "num_candidates": "1000"
                }
            }
        }
    }
}

# Select the query template based on the configuration
if config['query_type'] == 'base_query':
    selected_query_template = base_query_template
elif config['query_type'] == 'vector_query':
    selected_query_template = vector_query_template
elif config['query_type'] == 'hybrid_query':
    selected_query_template = hybrid_query_template
elif config['query_type'] == 'elser_query':
    selected_query_template = elser_query_template
else:
    raise ValueError("Invalid query type specified in the configuration file.")

for query in queries:
    request = {
        "id": query["query_id"],
        "template_id": "templated_query",
        "ratings": qrels.get(query["query_id"], []),
        "params": {
            "query_string": query["text"],
            "emb": query["emb"]
        },
        "templates": [selected_query_template]
    }
    rank_eval_requests["requests"].append(request)

# Save the rank evaluation requests to a JSON file
with open('rank_eval_requests.json', 'w') as f:
    json.dump(rank_eval_requests, f, indent=2)

print("Rank evaluation requests have been saved to 'rank_eval_requests.json'")

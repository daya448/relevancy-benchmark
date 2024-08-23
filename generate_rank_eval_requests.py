import json
import logging
from search_queries import get_search_query  # Import the query function

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to load JSON objects from a file where each JSON object is on a new line
def load_json_objects(filename):
    logging.info(f"Loading JSON objects from {filename}")
    json_objects = []
    try:
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
                        logging.error(f"Error decoding JSON: {obj}")
                        logging.error(f"Error message: {e}")
    except FileNotFoundError as e:
        logging.error(f"File not found: {filename}")
        logging.error(f"Error message: {e}")
    return json_objects

# Function to read the configuration from a file
def read_config(filename):
    logging.info(f"Reading configuration from {filename}")
    config = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split('=', 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError as e:
        logging.error(f"File not found: {filename}")
        logging.error(f"Error message: {e}")
    return config

# Load the configuration
config = read_config('config.txt')
query_types = config.get('query_types', '').split(',')
rating_threshold = int(config.get('relevant_rating_threshold'))

# Load the queries
queries = load_json_objects('queries-recall.json')

# Load the qrels from the qrels.tsv file
qrels = {}
try:
    with open(config['ratings_file']) as f:
        headers = f.readline().strip().split()  # Read and split the header line
        for line in f:
            row = line.strip().split()
            query_id, doc_id, rating = row[:3]
            if query_id not in qrels:
                qrels[query_id] = []
            rating = int(rating)
            if rating >= rating_threshold:
                qrels[query_id].append({
                    "_index": config['index_name'],
                    "_id": doc_id,
                    "rating": int(rating)
                })
except FileNotFoundError as e:
    logging.error(f"File not found: {config['ratings_file']}")
    logging.error(f"Error message: {e}")

rank_eval_requests = {
    "requests": []
}

for query_type in query_types:
    for query in queries:
        ratings = qrels.get(query["query_id"], [])
        k = max(1, len(ratings)*2)
        k = 100
        request = {
            "id": f"{query['query_id']}-{query_type}",  # Include query type in the ID
            "request": get_search_query(query_type, query_vector=query.get('emb'), query_string=query.get('text'), k=k),
            "ratings": ratings
        }
        rank_eval_request = {
            "requests": [request],
            "metric": {
                # "recall": {
                #     "k": k,
                #     "relevant_rating_threshold": rating_threshold,
                # }
                "dcg": {
                "k": k,
                "normalize": True
                }
            }
        }
        rank_eval_requests["requests"].append(rank_eval_request)

# Save the rank evaluation requests to a JSON file
output_file = 'rank_eval_requests.json'
try:
    with open(output_file, 'w') as f:
        json.dump(rank_eval_requests, f, indent=2)
    logging.info(f"Rank evaluation requests have been saved to '{output_file}'")
except IOError as e:
    logging.error(f"Error writing to file: {output_file}")
    logging.error(f"Error message: {e}")

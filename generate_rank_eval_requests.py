import json
from search_queries import get_search_query  # Import the query function
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

# Function to read the configuration from a file


def read_config(filename):
    config = {}
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split('=', 1)
                config[key.strip()] = value.strip()
    return config


# Load the configuration
config = read_config('config.txt')
query_type=config['query_type']

# Load the queries
queries = load_json_objects('queries.json')

# Load the qrels from the qrels.tsv file
qrels = {}
with open(config['ratings_file']) as f:
    headers = f.readline().strip().split()  # Read and split the header line
    for line in f:
        row = line.strip().split()
        query_id, doc_id, rating = row[:3]
        if query_id not in qrels:
            qrels[query_id] = []
        qrels[query_id].append({
            "_index": config['index_name'],
            "_id": doc_id,
            "rating": int(rating)
        })

rank_eval_requests = {
    "requests": []
}

for query in queries:
    request = {
        "id": query["query_id"],
        "request": get_search_query(query_type, query_vector=query.get('emb'), query_string=query.get('text')),
        "ratings": qrels.get(query["query_id"], [])
    }
    rank_eval_requests["requests"].append(request)

# Save the rank evaluation requests to a JSON file
with open('rank_eval_requests.json', 'w') as f:
    json.dump(rank_eval_requests, f, indent=2)

print("Rank evaluation requests have been saved to 'rank_eval_requests.json'")

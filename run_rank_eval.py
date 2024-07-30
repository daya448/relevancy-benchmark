import json
import csv
import requests

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

# Elasticsearch configuration
es_host = config['es_host']
api_token = config['api_token']
index_name = config['index_name']
benchmark_output_file = config['benchmark_output_file']
query_type = config['query_type']

# Load the rank evaluation requests from the JSON file
with open('rank_eval_requests.json', 'r') as f:
    rank_eval_requests = json.load(f)

# Prepare to write results to CSV
with open(benchmark_output_file, 'w', newline='') as csvfile:
    fieldnames = ['query_id', 'recall', 'query_type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate over each request in the judgement list
    for request in rank_eval_requests['requests']:
        request_id = request['id']
        # Define the rank evaluation request with the selected query template
        rank_eval_request = {
            "requests": [request],
            "metric": {
                "recall": {
                    "k": int(config['k']),
                    "relevant_rating_threshold": int(config['relevant_rating_threshold'])
                }
            }
        }

        try:
            # print(f"Response for request {rank_eval_request}")
            # Perform rank evaluation
            response = requests.post(
                f"{es_host}/{index_name}/_rank_eval",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"ApiKey {api_token}"
                },
                json=rank_eval_request
            )

            response_json = response.json()

            # Log the entire response for debugging
            print(
                f"Response for request {request_id}: {json.dumps(response_json, indent=2)}")

            # Check if 'details' key is in the response
            if response.status_code == 200 and 'details' in response_json:
                for result in response_json['details']:
                    recall = response_json['details'][result]['metric_score']
                    writer.writerow(
                        {'query_id': request_id, 'recall': recall,
                            'query_type': config['query_type']}
                    )
                print(
                    f"Rank evaluation results for request {request_id} saved to {benchmark_output_file}.")
            else:
                print(
                    f"Error: 'details' key not found in response for request {request_id}")
                print(f"Error details: {json.dumps(response_json, indent=2)}")

        except Exception as e:
            print(
                f"Error performing rank evaluation for request {request_id}: {e}")

print(f"All rank evaluation results saved to {query_type}_{benchmark_output_file}.")

import csv
import json
import logging
from es_client import get_elasticsearch_client, read_config

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Get the Elasticsearch client and configuration
logging.debug("Initializing Elasticsearch client and reading configuration.")
es = get_elasticsearch_client()
config = read_config('config.txt')

k = int(config['k'])
relevant_rating_threshold = int(config['relevant_rating_threshold'])
index_name = config['index_name']
benchmark_output_file = config['benchmark_output_file']

# Load the judgement list
logging.info("Loading judgement list from 'rank_eval_requests.json'.")
with open('rank_eval_requests.json') as f:
    judgement_list = json.load(f)

# Prepare to write results to CSV
logging.info(f"Writing benchmark results to '{benchmark_output_file}'.")
with open(benchmark_output_file, 'w', newline='') as csvfile:
    fieldnames = ['query_id', 'base_query',
                  'vector_query', 'hybrid_query', 'elser_query']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Prepare a dictionary to store recall scores
    recall_scores = {}

    # Iterate over each request in the judgement list
    for request in judgement_list['requests']:
        request_id = request['id']
        logging.debug(f"Processing request_id: {request_id}")

        # Split request_id to get query_id and query_type
        if '-' in request_id:
            query_id, query_type = request_id.rsplit('-', 1)
        else:
            logging.warning(
                f"Skipping request with malformed ID: {request_id}")
            continue

        # Define the rank evaluation request with the selected query template
        rank_eval_request = {
            "requests": [request],
            "metric": {
                "recall": {
                    "k": k,
                    "relevant_rating_threshold": relevant_rating_threshold,
                }
            }
        }

        try:
            # Perform rank evaluation
            response = es.rank_eval(index=index_name, body=rank_eval_request)
            logging.debug(
                f"Rank evaluation response for request_id {request_id}: {response}")

            # Extract results
            if response and 'details' in response:
                detail = response['details'].get(request_id, {})
                recall = detail.get('metric_score', 0)
                recall_rounded = round(recall, 2)

                # Store the recall score in the recall_scores dictionary
                if query_id not in recall_scores:
                    recall_scores[query_id] = {
                        'base_query': '',
                        'vector_query': '',
                        'hybrid_query': '',
                        'elser_query': ''
                    }
                recall_scores[query_id][query_type] = recall_rounded
            else:
                logging.error(
                    f"Unexpected response format for request {request_id}: {response}")

        except Exception as e:
            logging.error(
                f"Error performing rank evaluation for request {request_id}: {e}")

    # Write the recall scores to the CSV file
    for query_id, scores in recall_scores.items():
        writer.writerow({
            'query_id': query_id,
            'base_query': scores.get('base_query', ''),
            'vector_query': scores.get('vector_query', ''),
            'hybrid_query': scores.get('hybrid_query', ''),
            'elser_query': scores.get('elser_query', '')
        })

logging.info(
    f"All rank evaluation results saved to '{benchmark_output_file}'.")

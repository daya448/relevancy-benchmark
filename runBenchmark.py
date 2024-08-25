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

index_name = config['index_name']
benchmark_output_file = config['benchmark_output_file']
query_types = config.get('query_types', '').split(',')

# Load the judgement list
logging.info("Loading judgement list from 'rank_eval_requests.json'.")
with open('rank_eval_requests.json') as f:
    judgement_list = json.load(f)

# Prepare to write results to CSV
logging.info(f"Writing benchmark results to '{benchmark_output_file}'.")
with open(benchmark_output_file, 'w', newline='') as csvfile:
    fieldnames = query_types
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Prepare a dictionary to store recall scores
    metrics_scores = {}

    # Iterate over each request in the judgement list
    for request in judgement_list['requests']:
        request_id = request['requests'][0]['id']
        logging.debug(f"Processing request_id: {request_id}")

        # Split request_id to get query_id and query_type
        if '-' in request_id:
            query_id, query_type = request_id.rsplit('-', 1)
        else:
            logging.warning(
                f"Skipping request with malformed ID: {request_id}")
            continue
        
        # Define the rank evaluation request with the selected query template

        try:
            # Perform rank evaluation
            response = es.rank_eval(index=index_name, body=request, search_type="dfs_query_then_fetch")
            logging.debug(
                f"Rank evaluation response for request_id {request_id}: {response}")

            # Extract results
            if response and 'metric_score' in response:
                score = response.get('metric_score', 0)
                logging.info(f"Query type {query_type} returned score: {score}")
                score_rounded = round(score, 4)

               # Store the recall score in the recall_scores dictionary
                metrics_scores[query_type] = score_rounded
                
            else:
                logging.error(
                    f"Unexpected response format for request {request_id}: {response}")

        except Exception as e:
            logging.error(
                f"Error performing rank evaluation for request {request_id}: {e}")

    # Write the recall scores to the CSV file
    writer.writerow(metrics_scores)

logging.info(
    f"All rank evaluation results saved to '{benchmark_output_file}'.")

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
    fieldnames = ['query_id'] + query_types + ['rating_count'];
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Prepare a dictionary to store recall scores
    recall_scores = {}

    # Iterate over each request in the judgement list
    i = 0
    total_ratings = 0
    for request in judgement_list['requests']:
        i = i + 1
        request_id = request['requests'][0]['id']
        logging.debug(f"Processing request_id: {request_id}")

        # Split request_id to get query_id and query_type
        if '-' in request_id:
            query_id, query_type = request_id.rsplit('-', 1)
        else:
            logging.warning(
                f"Skipping request with malformed ID: {request_id}")
            continue
        
        rating_count = len(request['requests'][0]['ratings'])
        total_ratings = total_ratings + rating_count
        # Define the rank evaluation request with the selected query template

        try:
            # Perform rank evaluation
            print(index_name)
            response = es.rank_eval(index=index_name, body=request, search_type="dfs_query_then_fetch")
            # with open(str(i) + 'data.json', 'w') as file:
            #     json.dump(response.body, file, indent=4)
            logging.debug(
                f"Rank evaluation response for request_id {request_id}: {response}")

            # Extract results
            if response and 'metric_score' in response:
                #detail = response['details'].get(request_id, {})
                score = response.get('metric_score', 0)
                score_rounded = round(score, 5)

                # Store the recall score in the recall_scores dictionary
                if query_id not in recall_scores:
                    recall_scores[query_id] = {
                        'rating_count': rating_count
                    }
                recall_scores[query_id][query_type] = score_rounded
                
            else:
                logging.error(
                    f"Unexpected response format for request {request_id}: {response}")

        except Exception as e:
            logging.error(
                f"Error performing rank evaluation for request {request_id}: {e}")

    # Write the recall scores to the CSV file
    row_i = 0
    row_score_sum = {}
    for qtype in query_types:
        row_score_sum[qtype] = 0.0
    for query_id, scores  in recall_scores.items():
        row = {'query_id': query_id, 'rating_count': scores.get('rating_count', '')}
        row_i = row_i + 1
        for qtype in query_types:
            row[qtype] = scores.get(qtype, '')
            row_score_sum[qtype] = row_score_sum[qtype] + scores.get(qtype, 0)
        writer.writerow(row)
    avg_row = {}
    for qtype in query_types:
        avg_row[qtype] = row_score_sum[qtype] / row_i
    writer.writerow(avg_row)
    logging.info("Average number of ratings per request: " + str(total_ratings/i))

logging.info(
    f"All rank evaluation results saved to '{benchmark_output_file}'.")

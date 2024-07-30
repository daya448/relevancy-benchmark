import csv
import json
from es_client import get_elasticsearch_client,read_config

es = get_elasticsearch_client()
config = read_config('config.txt')



k = config['k']
relevant_rating_threshold = config['relevant_rating_threshold']
index_name = config['index_name']
benchmark_output_file = config['benchmark_output_file']



# Load the judgement list
with open('rank_eval_request.json') as f:
    judgement_list = json.load(f)

# Prepare to write results to CSV
with open(benchmark_output_file, 'w', newline='') as csvfile:
    fieldnames = ['query_id', 'recall', 'query_type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate over each request in the judgement list
    for request in judgement_list['requests']:
        request_id = request['id']

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
        print(rank_eval_request)
        try:
            # Perform rank evaluation
            response = es.rank_eval(
                index=index_name, body=rank_eval_request)

            # Extract results and write to CSV
            for result in response['details']:
                recall = response['details'][result]['metric_score']
                writer.writerow(
                    {'query_id': request_id, 'recall': recall, 'query_type': config['query_type']})

            print(
                f"Rank evaluation results for request {request_id} saved to {benchmark_output_file}.")

        except Exception as e:
            print(
                f"Error performing rank evaluation for request {request_id}: {e}")

print("All rank evaluation results saved to {}.".format(benchmark_output_file))

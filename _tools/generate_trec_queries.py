import pandas as pd
import requests
import json
import ndjson

# Configuration
es_host = 'https://ocbc-test.es.australia-southeast1.gcp.elastic-cloud.com:443'  # Replace with your Elasticsearch host
api_key = 'V3owWGZKRUI1c0JodXp4WHMyaXI6TVRhVEJqaUtURXVvSmZxdTlIODBFdw=='  # Replace with your Elasticsearch API key
model_id = 'sentence-transformers__all-mpnet-base-v2'
qrels_file = 'qrels_trec_covid.tsv'
input_file = 'trec_base_queries.json'
output_file = 'trec_queries.json'

# Function to get the vector from Elasticsearch
def get_vector(text):
    url = f'{es_host}/_ml/trained_models/{model_id}/_infer'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'ApiKey {api_key}'
    }
    payload = {
        "docs": [{"text_field": text}]
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    return result['inference_results'][0]['predicted_value']

with open(input_file, 'r') as f:
    reader = ndjson.reader(f)
    queries = list({query['_id']: query for query in reader}.values())  # Deduplicate by '_id'

# Open the output file
with open(output_file, 'w') as out_file:
    # Process each unique query
    for query in queries:
        query_id = query['_id']
        text = query['text']
        
        # Get the vector from Elasticsearch
        emb = get_vector(text)
        
        # Create the dictionary
        query_dict = {
            'query_id': query_id,
            'text': text,
            'emb': emb
        }
        
        # Write the dictionary to the NDJSON file
        out_file.write(json.dumps(query_dict) + '\n')

print(f'NDJSON output written to {output_file}')
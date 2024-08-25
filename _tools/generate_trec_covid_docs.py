from elasticsearch import Elasticsearch, helpers
import json

# Elasticsearch connection settings
es_host = "https://general-purpose.es.ap-southeast-2.aws.found.io:9243"  # Replace with your Elasticsearch host
index_name = "vdb910-reranking-test-trec-covid-embeddings-1"     # Replace with your index name
output_file_path = "output.ndjson"  # Path to the output NDJSON file
es_user = "your_username"          # Replace with your Elasticsearch username
es_password = "your_password"      # Replace with your Elasticsearch password
api_key = "RDJVTWVwRUJVQXNFQy12YXM5MmY6UTZVU1FMZmxSRzZwTUpxVlRyZ2VGQQ=="

# Create an Elasticsearch client with authentication
es = Elasticsearch(
    hosts=es_host,
    #http_auth=(es_user, es_password),  # Authentication credentials
    api_key=api_key,                 
    http_compress=True 
)

# Define a generator function to stream and process documents from Elasticsearch
def process_documents(es, index_name, max_docs=float('inf')):
    count = 0
    for doc in helpers.scan(
        es,
        index=index_name,
        _source=True,  # Only retrieve the _source field
        scroll="2m",  # Scroll timeout
        size=1000      # Number of documents per batch
    ):
        if count >= max_docs:
            break
        doc_source = doc['_source']
        
        # Rename 'emb.predicted_value' to 'emb'
        if 'emb' in doc_source and 'predicted_value' in doc_source['emb']:
            doc_source['emb'] = doc_source['emb'].pop('predicted_value')
        
        # Delete the field 'refresh'
        doc_source.pop('refresh', None)
        
        # Add the '_id' to the field 'docid'
        doc_source['docid'] = doc['_id']
        
        yield doc_source
        count = count + 1

# Open the NDJSON file for writing
with open(output_file_path, 'w') as ndjson_file:
    for doc_source in process_documents(es, index_name):
        # Write each processed document's _source as a JSON object in NDJSON format
        ndjson_file.write(json.dumps(doc_source) + '\n')

print(f"Documents have been successfully written to {output_file_path}")
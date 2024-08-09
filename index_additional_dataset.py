import json
from es_client import get_elasticsearch_client, read_config, helpers

# Elasticsearch connection details
es = get_elasticsearch_client()
config = read_config('config.txt')

# Specify the index name
index_name = config['index_name']

# Load the merged JSON file
with open("additional_dataset.json", 'r') as f:
    documents = json.load(f)

# Prepare the documents for bulk indexing
actions = [
    {
        "_index": index_name,
        "_source": doc
    }
    for doc in documents
]

# Perform the bulk indexing
helpers.bulk(es, actions)

print(f"Indexed {len(documents)} documents into {index_name}")

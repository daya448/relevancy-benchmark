# es_client.py

from elasticsearch import Elasticsearch

def read_config(file_path):
    config = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
                except ValueError:
                    print(f"Skipping malformed line: {line}")
    return config

def connect_elasticsearch(config):
    es = Elasticsearch(
        [config['es_host']],
        api_key=config['api_token'],
        verify_certs=True
    )
    if es.ping():
        print("Connected to Elasticsearch")
    else:
        print("Could not connect to Elasticsearch")
    return es

def get_elasticsearch_client():
    config = read_config('config.txt')
    return connect_elasticsearch(config)

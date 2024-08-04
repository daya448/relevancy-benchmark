from distutils.log import debug
import logging
from elasticsearch import Elasticsearch

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set the logging level for the elasticsearch transport logger to WARNING to avoid excess logging
logging.getLogger('elastic_transport.transport').setLevel(logging.CRITICAL)

def read_config(file_path):
    logging.info(f"Reading configuration from {file_path}")
    config = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    try:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
                    except ValueError:
                        logging.warning(f"Skipping malformed line: {line}")
    except FileNotFoundError as e:
        logging.error(f"Configuration file not found: {file_path}")
        logging.error(f"Error message: {e}")
    return config

def connect_elasticsearch(config):
    logging.debug(f"Connecting to Elasticsearch at {config.get('es_host')}")
    try:
        es = Elasticsearch(
            [config['es_host']],
            api_key=config['api_token'],
            verify_certs=True
        )
        if es.ping():
            logging.info("Connected to Elasticsearch")
        else:
            logging.error("Could not connect to Elasticsearch")
    except Exception as e:
        logging.error(f"Exception occurred while connecting to Elasticsearch: {e}")
        es = None
    return es

def get_elasticsearch_client():
    config = read_config('config.txt')
    return connect_elasticsearch(config)

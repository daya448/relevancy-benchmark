from elasticsearch import Elasticsearch

# Define the connection parameters
es_host = 'https://ocbc-vectorsearch-benchmarks.es.australia-southeast1.gcp.elastic-cloud.com'
es_port = 9243
api_token = 'eVVWdTNaQUJGdHR3Mnd6T2NTWVo6aERqT29BemFTRy1YZmdQTU85VmlTQQ=='

# Connect to Elasticsearch using the API token
es = Elasticsearch(
    [es_host],
    api_key=api_token,
    use_ssl=True,
    verify_certs=True
)
# Check if the connection is established
if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Could not connect to Elasticsearch")


# Define the template
template_name = 'knn_search_template'
template_body = {
    "script": {
        "lang": "mustache",
        "source": """
        {
          "query": {
            "knn": {
              "field": "{{field}}",
              "query_vector": "{{query_vector}}",
              "k": "{{k}}",
              "num_candidates": "{{num_candidates}}"
            }
          }
        }
        """
    }
}

# Store the template in Elasticsearch
es.put_script(id=template_name, body=template_body)
print("Template {template_name} created.")

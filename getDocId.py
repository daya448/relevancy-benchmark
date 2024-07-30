import csv
from es_client import get_elasticsearch_client,read_config

es = get_elasticsearch_client()
config = read_config('config.txt')
index_name = config['index_name']
input_file = config['input_file']
output_file = config['output_file']



def get_document_id_from_es(doc_id):
    query = {
        "query": {
            "term": {
                "docid": {
                    "value": doc_id
                }
            }
        }
    }
    try:
        response = es.search(index=index_name, body=query)
        print (query)
        if response['hits']['total']['value'] > 0:
            return response['hits']['hits'][0]['_id']
            print(f"Document with doc_id {doc_id} was found in in the index.")
        else:
            print(f"Document with doc_id {doc_id} not found in Elasticsearch.")
            return doc_id  # Return original doc_id if not found
    except Exception as e:
        print(f"Error searching for doc_id {doc_id} in Elasticsearch: {e}")
        return doc_id  # Return original doc_id if there's an error

# Load the qrels from the input TSV file
updated_rows = []
with open(input_file, 'r') as f:
    headers = f.readline().strip().split()  # Read and split the header line
    for line in f:
        row = line.strip().split()
        query_id, doc_id, rating = row[:3]
        new_doc_id = get_document_id_from_es(doc_id)
        updated_rows.append({
            "query_id": query_id,
            "doc_id": new_doc_id,
            "rating": rating,
            "ignore_field": row[3] if len(row) > 3 else ''  # Handle optional ignore_field
        })

# Write the updated rows to the output TSV file
with open(output_file, 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=["query_id", "doc_id", "rating", "ignore_field"], delimiter='\t')
    writer.writeheader()
    for row in updated_rows:
        writer.writerow(row)

print(f"Updated TSV file has been written to {output_file}")

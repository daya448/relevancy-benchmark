import ir_datasets

# Load the MSMARCO Passage v2 train qrels dataset
dataset = ir_datasets.load("msmarco-passage-v2/train")

# Get the qrels from the dataset
qrels = dataset.qrels_iter()
queries = dataset.queries_iter()
docs = dataset.docs_iter()

# Count the number of qrels
#qrels_count = sum(1 for _ in qrels)
qrels_count = dataset.qrels_count()
queries_count = dataset.queries_count()
docs_count = dataset.docs_count()


print(f"Total number of qrels in the MSMARCO Passage v2 train dataset: {qrels_count} and the queries: {queries_count} and docs: {docs_count}")


# with open("qrels.tsv", "w") as file:
#     # Write the header
#     file.write("query_id\tdoc_id\trelevance\n")
    
#     # Iterate over the qrels and write the first 100 to the file
#     for i, qrel in enumerate(dataset.qrels_iter()):
#         if i >= 100:
#             break
#         file.write(f"{qrel.query_id}\t{qrel.doc_id}\t{qrel.relevance}\n")

# print("First 100 qrels have been written to qrels.tsv")

with open("queries.json", "w") as file:
    # Write the header
    file.write("query_id\ttext\n")
    
    # Iterate over the qrels and write the first 100 to the file
    for i, queries in enumerate(dataset.queries_iter()):
        if i >= 100:
            break
        file.write(f"{queries.query_id}\t{queries.doc_id}\t{queries.relevance}\n")

print("First 100 queries have been written to queries.json")

# # Define the target docid
# target_docid = "msmarco_passage_00_0"
# # Flag to indicate if the docid is found
# docid_found = False

# # Iterate over the documents in the dataset
# for doc in dataset.docs_iter():
#     if doc.doc_id == target_docid:
#         docid_found = True
#         break

# # Print the result
# if docid_found:
#     print(f"Docid '{target_docid}' exists in the dataset.")
# else:
#     print(f"Docid '{target_docid}' does not exist in the dataset.")

# Measure the Recall

## Rank Evaluation API in Elaticsearch
The Ranking Evaluation API allows to evaluate the quality of ranked search results over a set of typical search queries. Given this set of queries and a list or manually rated documents, the `_rank_eval` endpoint calculates and returns typical information retrieval metric like Recall@K

For further on the API are available in the [documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-rank-eval.html)

## Data Used

This track benchmarks the dataset from [Cohere/msmarco-v2-embed-english-v3](https://huggingface.co/datasets/Cohere/msmarco-v2-embed-english-v3).

Given the size of this dataset 138.3M documents with 1024 dimension vectors you
need a cluster with at least 60GB of total RAM available to run performant HNSW queries.
The corpus contains the original 138M passages of the [MSMARCO (passage, version 2)](https://ir-datasets.com/msmarco-passage-v2.html) corpus embedded
into 1024 dimensional vectors with the [Cohere `embed-english-v3.0` model](https://cohere.com/blog/introducing-embed-v3).

## Relevance Ratings
For the relevance metrics, the `qrels.tsv` file contains annotations for all the queries listed in `queries.json`. This file is generated from the original training data available at [ir_datasets/msmarco_passage_v2](https://ir-datasets.com/msmarco-passage-v2.html#msmarco-passage-v2/train).




## Commands to use

For indexing additional data, containing the labelled answers, execute the below command. This expects the dataset should be available in the same folder as the script. Download from [google drive](https://drive.google.com/drive/folders/1-lUK_zJK-jnJqatX87vvm7JaA_VdDtlN) and place it in the same folder as script.

```
python3 index_additional_dataset.py
```


To generate rank_eval_requests with all the labelled answers, execute the below command. This should generate a file "rank_eval_requests.json"

```
python3 generate_rank_eval_requests.py
```

Run the benchmark query.This should generate a output file "benchmark_output.csv"

```
python3 runBenchmark.py
```

The above 2 scipts can be invoked by running single python file "run_customer_benchmark.py". This generates rank_eval requests and produces the  benchmark_output.csv file.

```
python3 run_customer_benchmark.py
```



## Output Summary

| query_id 	| base_query 	| vector_query 	| hybrid_query 	| elser_query 	|
|---	|---	|---	|---	|---	|
| 2000511 	| 0.12 	| 0.18 	| 0.18 	| - 	|
| 2056158 	| 0.01 	| 0.05 	| 0.028 	| - 	|



## Additional Notes

- Queries used for benchmarking are read using search_queries.py
- For the elser_query to work, field name "text_elser" should be generated using the field "text"


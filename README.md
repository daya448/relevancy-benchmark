# Demo for using Elasticsearch Ranking Evaluation API

The Ranking Evaluation API allows to evaluate the quality of ranked search results over a set of typical search queries. Given this set of queries and a list or manually rated documents, the `_rank_eval` endpoint calculates and returns typical information retrieval metric like Recall@K

For further on the API are available in the [documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-rank-eval.html)

## Data Used

This demo is based on a small subset of documents from the [English Wikipedia dump](https://dumps.wikimedia.org)
which is also available in an [Elasticsearch bulk format](https://dumps.wikimedia.org/other/cirrussearch/).
The relevance judgement data used for the evaluation is based on data collected in the Wikimedia labs [Discernatron Project](https://discernatron.wmflabs.org/login)
and is available for registered Wikimedia users for [download](https://discernatron.wmflabs.org/scores/all) separately. 

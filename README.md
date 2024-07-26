# Demo for using Elasticsearch Ranking Evaluation API

The Ranking Evaluation API allows to evaluate the quality of ranked search results over a set of typical search queries. Given this set of queries and a list or manually rated documents, the `_rank_eval` endpoint calculates and returns typical information retrieval metric like Recall@K

For further on the API are available in the [documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-rank-eval.html)

## Data Used

This demo is based on a small subset of documents from the [English Wikipedia dump](https://dumps.wikimedia.org)
which is also available in an [Elasticsearch bulk format](https://dumps.wikimedia.org/other/cirrussearch/).
The relevance judgement data used for the evaluation is based on data collected in the Wikimedia labs [Discernatron Project](https://discernatron.wmflabs.org/login)
and is available for registered Wikimedia users for [download](https://discernatron.wmflabs.org/scores/all) separately. 


#Commands to use
#To generate rank_eval_request with all the labelled answers.

```
python3 generateRankEvalRequest.py "Mary I Fergusson" "llajic" "JFK" "highliting text and calculations in word documents" "Picture resolution ppp" "homosexuality in the united states" "the great beer flood" "semper fight" "united broadband" "hydrostone halifax nova scotia" "antibacterial hand rub" "corona rhythm of the night" "dont cry guns n roses" "compare roads built Marcos and Aquino" "saab episodes" "who played the older dotti hilton in the movies in the movie a leage of their own" "298005 b.c." "mercedes truck w673" "ramoones" "red room tor sites" "ride bicycles" "german revolution" "latin dative" "Information Asymmetries" "SANTA CLAUS PRINT OUT 3D PAPERTOYS" "phasers on stun" "fort worth film" "Quiz Magic Academy" "naval flags" "tayps of wlding difats" "controls" "Adam Rapp"
```

#To run the benchmark query.It produces output in benchmark_output.csv.

```
python3 runBenchmark.py
```


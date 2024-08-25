import requests
import json

# Fetch the stopwords list
stopwords_list = requests.get("https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt").content
stopwords = set(stopwords_list.decode().splitlines())

# Remove apostrophes from each stopword
stopwords_no_apostrophes = [word.replace("'", "") for word in stopwords]

# Print the modified stopwords list in JSON format
print(json.dumps(stopwords_no_apostrophes, indent=2))
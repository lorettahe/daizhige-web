import urllib.request
import urllib.parse
import json
from os.path import join


class SearchResultItem(object):
    def __init__(self, path, title, highlight):
        self.path = path
        self.title = title
        self.highlight = highlight


def combine_search(search_token):
    return '"{0}"'.format(search_token)


def search_for_terms(terms, offset):
    search_tokens = terms.split(" ")
    real_search_str = " ".join([combine_search(token) for token in search_tokens])
    params = {"q": real_search_str,
              "wt": "json",
              "indent": "true",
              "start": str(offset),
              "hl": "true",
              "hl.fl": "article",
              "hl.simple.pre": "<strong>",
              "hl.simple.post": "</strong>"}
    url_values = urllib.parse.urlencode(params)
    full_url = "http://localhost:8983/solr/daizhige/select?" + url_values
    with urllib.request.urlopen(full_url) as response:
        solr_response = response.read().decode("utf-8")
        solr_response_obj = json.loads(solr_response)
        num_found = solr_response_obj["response"]["numFound"]
        actual_responses = solr_response_obj["response"]["docs"]
        results = []
        for doc in actual_responses:
            doc_id = doc["id"]
            path = join(join(*doc["categories"]), doc["name"]+".txt")
            highlight = solr_response_obj["highlighting"][doc_id]["article"][0]
            results.append(SearchResultItem(path, doc["name"], highlight))
    return [num_found, results]

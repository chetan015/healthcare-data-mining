import pysolr

class searchModel():
    def __init__(self):
        # Create a client instance. The timeout and authentication options are not required.
        self.limit_result = 10
        self.solr = pysolr.Solr('http://localhost:8983/solr/healthcare', always_commit=True)
        
    def fetch(self, query_object):
        results = []
        query_type = query_object["query_type"]
        query_term = query_object["query_term"]
        query_site = query_object["query_site"]
        if(query_site is None):
            filter_queries = query_type + ':' + query_term + ' OR content:' + query_term + ' OR heading:' + query_term + ' OR group:' + query_term
        else:
            filter_queries = '(site:' + query_site + ') AND (' + query_type + ':' + query_term + ' OR content:' + query_term + ' OR heading:' + query_term + ' OR group:' + query_term + ')'

        results += self.solr.search(q=filter_queries, **{
                'fl': '* score'
            }, rows = self.limit_result)
        return results
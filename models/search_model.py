import pysolr

class searchModel():
    def __init__(self):
        # Create a client instance. The timeout and authentication options are not required.
        self.solr = pysolr.Solr('http://localhost:8983/solr/healthcare', always_commit=True)
        
    def fetch(self, query_object):
        results = []

        filter_queries = query_object["query_type"] + ':' + query_object["query_term"]
        results += self.solr.search(q=filter_queries, **{
                'fl': '* score'
            })

        # if query_object["q_disease"] and query_object["q_symptom"]:
        #     disease_query = query_object["q_disease"]
        #     symptom_query = query_object["q_symptom"]
        #     filter_queries = ['Content:' + disease_query, 'Content:' + symptom_query]
        #     results += self.solr.search(fq=filter_queries)

        # elif query_object["q_disease"]:
        #     disease_query = query_object["q_disease"]
        #     filter_queries = ['Content:' + disease_query]
        #     results += self.solr.search(fq=filter_queries)

        # elif query_object["q_symptom"]:
        #     symptom_query = query_object["q_symptom"]
        #     results += self.solr.search(fq=filter_queries)

        # else:
        #     results += self.solr.search(q="*:*")
        return results
import pysolr
import json
# import jsonlines

# Create a client instance. The timeout and authentication options are not required.
solr = pysolr.Solr('http://localhost:8983/solr/healthcare', always_commit=True)

# How you'd index data.
def create():
    # solr.add([
    #             {
    #                 "id": "doc_1",
    #                 "title": "A test document",
    #                 "number": 22387237.0,
    #             },
    #             {
    #                 "id": "doc_2",
    #                 "title": "The Banana: Tasty or Dangerous?",
    #                 "number": 3223.0,
    #             },
    #         ])

    # data = []
    with open('../data/medhelp_mm.jl') as f:
        for line in f:
            try:
                # print([json.loads(line)])
                # break
                # data.append(json.loads(line))
                solr.add([json.loads(line)])
            # solr.add(line)
            except Exception as e: 
                print(e)

    # print(data) 
    # solr.add(data)

def delete():
    solr.delete(q='*:*')

def search(term):
    filter_queries = 'content:' + term
    print(filter_queries)
    results = solr.search(q="*:*")
    print("Saw {0} result(s).".format(len(results)))
    for result in results:
        print(result)

create()
# search('cancer')
# delete()

# You can index a parent/child document relationship by
# associating a list of child documents with the special key '_doc'. This
# is helpful for queries that join together conditions on children and parent
# documents.

# Later, searching is easy. In the simple case, just a plain Lucene-style
# # query is fine.
# results = solr.search(q='*:*')

# print("Saw {0} result(s).".format(len(results)))
# # print(results)
# for result in results:
#     print(result)
    # print(result['id'])

# # # The ``Results`` object stores total results found, by default the top
# # # ten most relevant results and any additional data like
# # # facets/highlighting/spelling/etc.
# print("Saw {0} result(s).".format(len(results)))

# # # Just loop over it to access the results.
# for result in results:
#     print("The title is '{0}'.".format(result['title']))
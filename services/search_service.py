import pysolr
import json

from os import path
import sys
sys.path.append(path.abspath('../models'))
from search_model import searchModel

# from project.model.search_model import search_model

class SearchService():
    def __init__(self):
        self.search_model = searchModel()
        
    def search(self, queries):
        results = self.search_model.fetch(queries)
        return results
        # return self.rank_posts(results)
    
    def rank_posts(self, posts):
        res = []
        # i = 0
        for post in posts:
            final_score = post["score"] + post["trustworthiness"] + post["freshness"] + post["hotness"] + post["length"]
            post["final_score"] = final_score
            # i += 1
            res.append(post)
        res = sorted(res, key=lambda x:x['final_score'], reverse = True)
        return res
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
        result = self.normalize(posts)
        for post in result:
            final_score = post["score"] + post["trustworthiness"] + post["freshness"] + post["hotness"] + post["normalized-length"]
            post["final_score"] = final_score
            # i += 1
            res.append(post)
        res = sorted(res, key=lambda x:x['final_score'], reverse = True)
        return res

    def normalize(self,posts):
        time_created = []
        no_of_replies =[]
        lengths = []
        author_weights = []
        posts_ = []
        tf_idf = []
        for post in posts:
            post=json.loads(post)
            time_created.append(post["lastActivityTs"])
            no_of_replies.append(post['numExpertReplies'])
            lengths.append(post['numWords'])
            author_weights.append(post['authorsWeight'])
            posts_.append(post)
            tf_idf.append(posts['score'])
        
        #freshness
        maxTime = max(time_created)
        sf = [val/maxTime for val in time_created]
        
        #hotness
        maxReplies = max(no_of_replies)
        sh = [val/maxReplies for val in no_of_replies]
        
        #length
        max_smr = max(tf-idf)
        max_length = max(lengths)
        length_posts = [((lengths[i]/max_length)*max_smr)for i in range(len(lengths))]
        
        #trusthworthiness
        st = [(author_weights[i]*max_smr) for i in range(len(author_weights))]
        max_st = max(st)
        st_normalized =[(val/max_st) for val in st]

        i = 0

        for post in posts_:
            post['freshness'] = sf[i]
            post['hotness'] = sh[i]
            post['normalized-length'] = length_posts[i]
            post['trusthworthiness'] = st_normalized[i]
            i+=1
            
        return posts_

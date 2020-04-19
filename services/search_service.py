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
        result = self.normalize(posts)
        final_scores = []
        for post in result:
            final_score = 3.5*post["tf-idf-score"] + 2.25*post["trustworthiness"] + post["freshness"] + 2.5*post["hotness"] + 0.75*post["normalized-length"]
            final_scores.append(final_score)
        print(final_scores)
        max_fs = max(final_scores)

        for i in range(len(result)):
            result[i]["final_score"] = final_scores[i]/max_fs
            res.append(result[i])
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
            time_created.append(post["lastActivityTs"][0])
            no_of_replies.append(post['numExpertReplies'][0])
            lengths.append(post['numWords'][0])
            author_weights.append(post['authorsWeight'][0])
            posts_.append(post)
            tf_idf.append(post['score'])
        
        #freshness
        maxTime = max(time_created)
        sf = [val/maxTime for val in time_created]
        
        #hotness
        maxReplies = max(no_of_replies)
        sh = [val/maxReplies for val in no_of_replies]
        
        #nomalizing tf-idf
        
        max_smr = max(tf_idf)
        tf_idf_normalized = [(tf/max_smr) for tf in tf_idf]
        
        #length
        max_length = max(lengths)
        length_posts = [((lengths[i]/max_length)*max_smr)for i in range(len(lengths))]
        
        #trustworthiness
        st = [(author_weights[i]*max_smr) for i in range(len(author_weights))]
        max_st = max(st)
        st_normalized =[(val/max_st) for val in st]



        i = 0
        for post in posts_:
            post['freshness'] = sf[i]
            post['hotness'] = sh[i]
            post['normalized-length'] = length_posts[i]
            post['trustworthiness'] = st_normalized[i]
            post['tf-idf-score'] =tf_idf_normalized[i]
            i+=1
            
        return posts_
    
    def metamap_analysis(self,posts):
        symptomsdict={}
        treatmentsdict={}
        for post in posts:
            if len(obj['symptoms']) > 0:
                for symptoms in obj['symptoms']:
                    if symptoms not in symptomsdict:
                        symptomsdict[symptoms]=1
                    else:
                        symptomsdict[symptoms]+=1
                    if len(obj['treatments']) > 0:

                for treatments in obj['treatments']:
                    if treatments not in treatmentsdict:
                        treatmentsdict[treatments]=1
                    else:
                        treatmentsdict[treatments]+=1
        return symptomsdict,treatmentsdict


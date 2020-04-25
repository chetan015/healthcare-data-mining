import csv,numpy as np,sys,operator,pickle
from numpy.linalg import inv
np.set_printoptions(threshold=sys.maxsize)

class sympgraphModel():
    def __init__(self):
        # Create a client instance. The timeout and authentication options are not required.
        pass

    def pagerank(self, inversematrix, seed):
	    return np.dot(inversematrix,seed)

    def fetch(self, query):
        try:
            Tinfile = open("../data/Tmatrixinversefile","rb")
            Sinfile = open("../data/symptomsfile","rb")
            seedfile = open("../data/seedfile","rb")

            inverse = pickle.load(Tinfile)
            symptomlist = pickle.load(Sinfile)
            seed = pickle.load(seedfile)
            seed = 0.15*seed
            index = symptomlist.index(query)
            seed[index] = 1

            finalrank = self.pagerank(inverse,seed)

            rankdictionary={}
            for symptom,rank in zip(symptomlist,finalrank):
                rankdictionary[symptom] = rank

            sorted_x = sorted(rankdictionary.items(),key = operator.itemgetter(1), reverse = True)

            symptoms = []
            for key, val in sorted_x[:10]:
                symptoms.append(key)

            return symptoms
        except Exception as e:
            print(e)
            return []

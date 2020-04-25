import csv,numpy as np,sys,operator,pickle
from numpy.linalg import inv
np.set_printoptions(threshold=sys.maxsize)
	

def pagerank(inversematrix,seed):
	return np.dot(inversematrix,seed)


def main(query):
	Tinfile = open("Tmatrixinversefile","rb")
	Sinfile = open("symptomsfile","rb")
	seedfile = open("seedfile","rb")
	inverse = pickle.load(Tinfile)
	symptomlist = pickle.load(Sinfile)
	seed = pickle.load(seedfile)
	seed = 0.15*seed
	# query ="nausea"
	index = symptomlist.index(query)
	seed[index] = 1
	finalrank = pagerank(inverse,seed)
	rankdictionary={}
	for symptom,rank in zip(symptomlist,finalrank):
		rankdictionary[symptom] = rank
	#print(rankdictionary)
	sorted_x = sorted(rankdictionary.items(),key = operator.itemgetter(1), reverse = True)
	#print(sorted_x)
	print(sorted_x[:20])
	#for key,val in sorted_x:
	#	print(key)

main("nausea")
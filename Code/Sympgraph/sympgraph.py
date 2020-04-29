import csv,numpy as np,sys,operator,pickle
from numpy.linalg import inv
np.set_printoptions(threshold=sys.maxsize)

def readfiles():
	dataset_file = open("combineddatasetoutput.csv")
	symptoms_file = open("symptomlistoutput.csv")
	dataset_reader = csv.reader(dataset_file)
	symptom_reader = csv.reader(symptoms_file)
	symptomlist =[]
	for reader in symptom_reader:
		symptomlist = list(reader)
		#print(reader)
	symptomlist.pop()
	print(symptomlist)
	print(len(symptomlist))
	return dataset_reader,symptom_reader

def create_symptomlist(symptoms_reader):
	symptomlist =[]
	for reader in symptoms_reader:
		symptomlist = list(reader)
	symptomlist.pop()
	return symptomlist

def create_postdictionary(dataset_reader):
	postdictionary={}
	for reader in dataset_reader:
		if reader[0] not in postdictionary:
			postdictionary[reader[0]] = reader[1:]
	print(postdictionary)
	return postdictionary



def create_matrix(symptomlistsize,noofposts):
	return np.zeros((symptomlistsize,noofposts))

def fill_matrix(matrix,symptomlist,postdictionary):
	for key,val in postdictionary.items():
		if len(val) > 0:
			for items in val:
				if items != '':
					matrix[symptomlist.index(items)][int(key)-1]+=1
	return matrix

def normalize_matrix(matrix):
	transposematrix = matrix.transpose()
	print("The transpose changes to %s" % transposematrix)
	print(type(matrix))
	dotproductmatrix = np.dot(matrix,transposematrix)
	print("The dot product between matrix and transposematrix is %s" % dotproductmatrix)
	x_normed = dotproductmatrix /dotproductmatrix.sum(axis=0)
	print("The matrix after normalizing is %s" % x_normed)
	x_normed[np.isnan(x_normed) | np.isinf(x_normed)]=0
	print("The matrix after removing nan and inf is %s" % x_normed)
	print(x_normed.shape)
	return x_normed

def create_identity_matrix(size):
	return np.identity(size)

def pagerank(Tmatrix,identity_matrix,alpha):
	alphamatrix = alpha *Tmatrix

	minus = identity_matrix - alphamatrix
	invresult = inv(minus)
	return invresult

def process():
	dataset_file = open("combineddatasetoutput.csv")
	symptoms_file = open("symptomlistoutput.csv")
	dataset_reader = csv.reader(dataset_file)
	symptom_reader = csv.reader(symptoms_file)
	symptomlist = create_symptomlist(symptom_reader)
	postdictionary = create_postdictionary(dataset_reader)
	matrix = create_matrix(629,7050)
	resultmatrix = fill_matrix(matrix,symptomlist,postdictionary)
	Tmatrix = normalize_matrix(resultmatrix)
	identity_matrix = create_identity_matrix(629)
	S = np.zeros((629,1))
	alpha = 0.85
	inverseresult = pagerank(Tmatrix,identity_matrix,0.85)
	betaval = 1 - alpha
	betaseed = betaval * S
	finalrank = np.dot(inverseresult,betaseed)
	rankdictionary={}
	for symptom,rank in zip(symptomlist,finalrank):
		rankdictionary[symptom] = rank
	print(rankdictionary)
	sorted_x = sorted(rankdictionary.items(),key = operator.itemgetter(1), reverse = True)
	print(sorted_x)
	for key,val in sorted_x:
		print(key)

	tfile = open("Tmatrixinversefile","wb")
	pickle.dump(inverseresult,tfile)
	tfile.close()
	sfile = open("symptomsfile","wb")
	pickle.dump(symptomlist,sfile)
	sfile.close()
	seedfile = open("seedfile","wb")
	pickle.dump(S,seedfile)
	seedfile.close()

if __name__ == "__main__":
	process()




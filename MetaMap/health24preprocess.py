import json,ast, metamap
from textblob import TextBlob
from datetime import datetime
import time

metamapobj = metamap.MyMetaMap()
path = metamapobj.metamap_path

'''
def freshness(timeRes):
	maxVal = max(timeRes)
	sf = [val/maxVal for val in timeRes]
	return sf
'''

file = open("testdata.jl","r")
file = file.read()
file = file.split("\n")
finalString=""
i=1
#time_list = []
for obj in file:
	print("Processing for row %d" % i)
	dataset = []
	obj = json.loads(obj)
	totalcontent =obj['content']
	if obj['replies']:
		#size = len(obj['replies'])
		size = obj['numReplies']
		d = datetime.strptime(obj['replies'][size-1]['created'], "%Y/%m/%d")
		time_val = time.mktime(d.timetuple())
		for replies in obj['replies']:
			totalcontent+=replies['content']
	else:
		d = datetime.strptime(obj['created'], "%Y/%m/%d")
		time_val = time.mktime(d.timetuple())
	totalcontent = totalcontent.encode("ascii", errors="ignore").decode()
	dataset.append(totalcontent)
	count = len(totalcontent.split(" "))

	result = metamapobj.metamap(path,dataset)
	symptomlist=[]
	diseaselist=[]
	treatmentlist=[]
	clinicaldruglist=[]
	bodypartlist =[]
	for key,val in result.items():
		if 'dsyn' in val:
			diseaselist.append(key)

		if 'sosy' in val:
			symptomlist.append(key)

		if 'topp' in val:
			treatmentlist.append(key)

		if 'clnd' in val:
			clinicaldruglist.append(key)

		if 'bpoc' in val:
			bodypartlist.append(key)

	obj['timestamp'] = time_val
	obj['disease'] = diseaselist
	obj['symptom'] = symptomlist
	obj['treatment'] = treatmentlist
	obj['clinicaldrug'] = clinicaldruglist
	obj['affectedbodypartlist'] = bodypartlist
	obj['noofexpertreplies'] = obj["numReplies"]
	obj['lengthofpost'] = count
	finalString += json.dumps(obj)
	finalString+="\n"
	#print(finalString)
	i+=1
#sf = freshness(time_list)
with open("testdatanew.jl","w+") as f:
	f.write(finalString)
	f.close()

'''
with open("testdatanew.jl","r") as f, open("testdatanew.jl","w") as k:
	f.readlines()
	#f.split("\n")
	j=0
	for obj in f:
		obj = json.loads(obj)
		obj['freshnessScore'] = sf[j]
		j+=1
	f.close()
'''

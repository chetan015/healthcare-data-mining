import json,ast, testmetamap
from datetime import datetime
import time

metamapobj = testmetamap.MyMetaMap()
path = metamapobj.metamap_path

file = open("testdatamedhelp.jl","r")
file = file.read()
file = file.split("\n")
finalString=""
i=1
#time_list = []
for obj in file:
	print("Processing for row %d" % i)
	dataset = []
	obj = json.loads(obj)
	#print(obj['replies'][0]['created'])
	
	#print(obj['replies'][0]['created'])
	#d = datetime.strptime(obj['replies'][0]['created'], "%Y-%m-%d %H:%M:%S%z")
	#print(d)
	#time_val = time.mktime(d.timetuple())
	#print(time_val)
	#print(obj)
	totalcontent =obj['content']
	count = len(totalcontent.split(" "))
	noofexpertreplies=0
	if obj['numReplies'] > 0:
		#size = len(obj['replies'])
		obj['replies'][0]['created'] = obj['replies'][0]['created'].replace("T"," ")
		size = obj['numReplies']
		d = datetime.strptime(obj['replies'][size-1]['created'], "%Y-%m-%d %H:%M:%S%z")
		time_val = time.mktime(d.timetuple())
		for replies in obj['replies']:
			if replies[expert] == True:
				noofexpertreplies+=1
				totalcontent+=replies['content']
				count+=len(totalcontent.split(" "))
	else:
		noofexpertreplies=0
		d = datetime.strptime(obj['created'], "%Y-%m-%d %H:%M:%S%z")
		time_val = time.mktime(d.timetuple())

	totalcontent = totalcontent.encode("ascii", errors="ignore").decode()
	dataset.append(totalcontent)
	#count = len(totalcontent.split(" "))

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

	obj['timestamp'] = time_val #timestamp
	obj['disease'] = diseaselist
	obj['symptom'] = symptomlist
	obj['treatment'] = treatmentlist
	obj['clinicaldrug'] = clinicaldruglist
	obj['affectedbodypartlist'] = bodypartlist
	obj['noofexpertreplies'] = noofexpertreplies #hotness
	obj['lengthofpost'] = count #lengthofpost
	finalString += json.dumps(obj)
	finalString+="\n"
	#print(finalString)
	i+=1
#sf = freshness(time_list)
with open("testdatamedhelpout.jl","w+") as f:
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

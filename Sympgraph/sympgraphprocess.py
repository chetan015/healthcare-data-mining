import json,os


def extractsymptoms(line):
	return line['symptoms']

with open("symptomlistoutput.csv","w+") as out_symptom:
	with open("combineddatasetoutput.csv","w+") as out_file:
		with open("combineddataset.jl") as in_file:
			i=1
			finalstring = ""
			uniquesymptomslist=[]
			for line in in_file:
				print("Processing post %d" %i)
				data = json.loads(line)
				symptomlist = extractsymptoms(data)
				if len(symptomlist) > 0:
					for symptoms in symptomlist:
						finalstring+=symptoms+","
					finalstring = finalstring[:-1]
				if len(symptomlist) > 0:
					for symptoms in symptomlist:
						if symptoms not in uniquesymptomslist:
							out_symptom.write(symptoms+",")
							uniquesymptomslist.append(symptoms)
				out_file.write(str(i)+","+finalstring+"\n")
				finalstring=""
				i+=1
				out_file.flush()
				out_symptom.flush()
				os.fsync(out_file)
				os.fsync(out_symptom)
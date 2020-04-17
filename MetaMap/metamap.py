from pymetamap import MetaMap
import string




class MyMetaMap:
	def __init__(self):
		self.configuration_file = open("/Users/nipunmediratta/Desktop/CSE-573-healthcare-data-mining/MetaMap/metamap.cfg","r")
		self.configuration_file_contents = self.configuration_file.read()
		self.metamap_path = self.configuration_file_contents.split("=")[1]
		self.configuration_file.close()

	def metamap(self,path,dataset):
		semantic_types ={}
		length = len(dataset)
		indices = [i+1 for i in range(len(dataset))]
		mm = MetaMap.get_instance(path)
		concepts,error = mm.extract_concepts(dataset,indices)
		if not error:
			for concept in concepts:
				if concept.__class__.__name__ is not "ConceptAA":
					semantic_types[concept.preferred_name] = concept.semtypes
			return semantic_types

'''
def metamap(path,dataset):
	semantic_types ={}
	length = len(dataset)
	indices = [i+1 for i in range(len(dataset))]
	mm = MetaMap.get_instance(path)
	concepts,error = mm.extract_concepts(dataset,indices)
	if not error:
		for concept in concepts:
			semantic_types[concept.preferred_name] = concept.semtypes
		return semantic_types


def main():
	configuration_file = open("/Users/nipunmediratta/Desktop/CSE-573-healthcare-data-mining/MetaMap/metamap.cfg","r")
	configuration_file_contents = configuration_file.read()
	metamap_path = configuration_file_contents.split("=")[1]
	configuration_file.close()
	#metamap_path = input("Please enter the path where your metamap binary file is located")
	dataset = ['I have Diabetes and I cough a lot', 'John had a huge heart attack']
	#semantic_types = 
	metamap(metamap_path,dataset)
	#print(semantic_types)
'''

#main()
#dataset = ["Hi Doctor. My Daughter Has nose bleeds, usually during a cold or sinus related issue. It is the left nostril that is a problem. We have been using Naseptin cream after it happen\u2019s, to help it heal. What else can we do to prevent it from happening?"]
#datasetlist=[]
#dataset = "I have my blood work done every six months and last time my A1C was 7.9 and was diagnosed with type II diabetes. I was put on metformin 2 X 500 twice a day but only took one pill with breakfast. My fasting glucose was still greater than 7. After three months on metformin my A1C was 7.3. Now I heard about Intermittent Fasting (IF) and have been trying 16/8 for the last four  weeks and have lost  4 lbs. I am a very active person at the gym. Work out 4-5 times a week cardio and strength training. Healthy dietary habits. Since IF I am no longer taking metformin and want to control my diabetes through diet and exercise. The only problem is although my fasting glucose is lower than when I was on metformin but it is still in 7-9 range. Is this normal when you are doing IF? During the day it gets normal. After meals its between 6-8.5. The high fasting glucose still concerns me but I really do not want to go on medicine and I do eat healthy and am determined to lose the extra 10 pounds I need to lose. I am 5\u2019 and weigh 135lbs and want to lose 10 pounds. Should I go back on metformin or continue doing what I am doing. Hi"
#dataset = dataset.encode("ascii", errors="ignore").decode()
#datasetlist.append(dataset)
#print(datasetlist)

#dataset ="I have food intolerance. I saw a Kinesiologist who appears to have diagnosed the reasons why and advised a supplement that contains maltodextrin which I cannot tolerate. As the enzymes in the product are meant to cure my problem - would you advise that I continue with the supplement despite the very uncomfortable side-effects from maltodextrin?"
#dataset = dataset.encode("ascii", errors="ignore").decode()
#datasetlist.append(dataset)

#dataset =  " I have my blood work done every six months and last time my A1C was 7.9 and was diagnosed with type II diabetes. I was put on metformin 2 X 500 twice a day but only took one pill with breakfast. My fasting glucose was still greater than 7. After three months on metformin my A1C was 7.3. Now I heard about Intermittent Fasting (IF) and have been trying 16/8 for the last four  weeks and have lost  4 lbs. I am a very active person at the gym. Work out 4-5 times a week cardio and strength training. Healthy dietary habits. Since IF I am no longer taking metformin and want to control my diabetes through diet and exercise. The only problem is although my fasting glucose is lower than when I was on metformin but it is still in 7-9 range. Is this normal when you are doing IF? During the day it gets normal. After meals its between 6-8.5. The high fasting glucose still concerns me but I really do not want to go on medicine and I do eat healthy and am determined to lose the extra 10 pounds I need to lose. I am 5\u2019 and weigh 135lbs and want to lose 10 pounds. Should I go back on metformin or continue doing what I am doing. "
#dataset = dataset.encode("ascii", errors="ignore").decode()
#datasetlist.append(dataset)
#metamapobj = MyMetaMap()
#print(type(metamapobj))
#result = metamapobj.metamap(metamapobj.metamap_path,datasetlist)
#print(result)




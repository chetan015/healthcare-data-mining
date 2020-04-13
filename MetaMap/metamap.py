from pymetamap import MetaMap

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
	configuration_file = open("metamap.cfg","r")
	configuration_file_contents = configuration_file.read()
	metamap_path = configuration_file_contents.split("=")[1]
	configuration_file.close()
	#metamap_path = input("Please enter the path where your metamap binary file is located")
	dataset = ['I have Diabetes and I cough a lot', 'John had a huge heart attack']
	semantic_types = metamap(metamap_path,dataset)
	print(semantic_types)

main()



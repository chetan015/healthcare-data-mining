from pymetamap import MetaMap

def metamap(path,dataset):
	length = len(dataset)
	indices = [i+1 for i in range(len(dataset))]
	mm = MetaMap.get_instance(path)
	concepts,error = mm.extract_concepts(dataset,indices)
	if not error:
		return concepts


def main():
	metamap_path = input("Please enter the path where your metamap binary file is located")
	dataset = ['Heart Attack', 'John had a huge heart attack']
	concepts = metamap(metamap_path,dataset)
	for concept in concepts:
		print(concept)

main()



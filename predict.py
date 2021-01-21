import argparse
import csv
import pickle
from sklearn import svm

def parse_features(string_feature):
	# Take in as '[0, 0, 0, 1]' and parse into list
	list_features = string_feature[1:len(string_feature)-1]
	list_features = list_features.split(', ')
	for i in range(len(list_features)):
		list_features[i] = float(list_features[i])
	return list_features

def run(args):
	
	model_path = args.model_path
	test_file = args.test_file

	clf = pickle.load(open(model_path, 'rb'))
	testX = []

	count = 1
	ids = []
	with open(test_file, mode='r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			testX.append(parse_features(row['Features']))
			ids.append(row['IDs'])
	
	print("Constructed testing dataset")
	testY = clf.predict(testX) # Use same feature builder and new data
	print("Done testing dataset")
	path_dir = "results/" + test_file.split('.')[0].split('/')[1] + ".csv"
	result_file = open(path_dir, 'w')

	csvwriter = csv.writer(result_file, delimiter=',')
	csvwriter.writerow(['Test Label', 'ID'])

	assert len(testY) == len(ids)
	for i in range(len(testY)):
		csvwriter.writerow([testY[i], ids[i]])
	print("Successfully wrote results to file in results")
	count += 1

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
        'Build data file from social media posts')
	parser.add_argument('--model_path', type=str)
	parser.add_argument('--test_file', type=str)
	args = parser.parse_args()
	run(args)
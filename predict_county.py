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

	counties = []

	with open(test_file, mode='r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			testX.append(parse_features(row['Features']))
			counties.append((row['County'], row['State']))
	
	print("Constructed testing dataset")
	testY = clf.predict(testX) # Use same feature builder and new data
	print("Done testing dataset")
	path_dir = "results/" + test_file.split('.')[0].split('/')[1] + ".csv"
	result_file = open(path_dir, 'w')

	csvwriter = csv.writer(result_file, delimiter=',')
	csvwriter.writerow(['County','Predicted Turnout'])

	assert len(testY) == len(counties)
	for i in range(len(testY)):
		csvwriter.writerow([counties[i], testY[i]])
	print("Successfully wrote results to file in results")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
        'Build data file from social media posts')
	parser.add_argument('--model_path', type=str, default='models/2016_gov_agencies_model')
	parser.add_argument('--test_file', type=str, default='social_data/2020_gov_agencies_data_county.csv')
	args = parser.parse_args()
	run(args)
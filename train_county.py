import argparse
import pickle
import csv
from sklearn import svm

def parse_features(string_feature):
	# Take in as '[0, 0, 0, 1]' and parse into list
	list_features = string_feature[1:len(string_feature)-1]
	list_features = list_features.split(', ')
	for i in range(len(list_features)):
		list_features[i] = float(list_features[i])
	return list_features

def run(args):
	file_path = args.file_path
	model_path = args.model_path
	labels_path = args.labels_path

	trainX = []
	trainY = []

	data = {} # map (county, state) to trainX
	labels = {} # map (county, state) to trainY
	with open(file_path, mode='r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			data[(row['County'], row['State'])] = parse_features(row['Features'])
	with open(labels_path, mode='r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			labels[(row['county'], row['state'])] = row['turnout rate']

	for key in data.keys():
		try:
			trainY.append(labels[key])

			trainX.append(data[key])
		except KeyError:
			print(str(key) + "not found")

	print("Done constructing training data")
	clf = svm.SVC(kernel='linear')
	clf.fit(trainX, trainY) # training

	print("Done training model")
	pickle.dump(clf, open(model_path, 'wb'))

	print("Saved model successfully")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
        'Train model on data')
	parser.add_argument('--file_path', type=str, default='social_data/2016_gov_agencies_data_county.csv')
	parser.add_argument('--model_path', type=str, default='models/2016_gov_agencies_model')
	parser.add_argument('--labels_path', type=str, default='voter_data/2016_voter_data.csv')
	args = parser.parse_args()
	run(args)
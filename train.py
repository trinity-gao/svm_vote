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

	trainX = []
	trainY = []
	with open(file_path, mode='r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			trainX.append(parse_features(row['Features']))
			trainY.append(row['Labels'])

	print("Done constructing training data")
	clf = svm.SVC(kernel='linear')
	clf.fit(trainX, trainY) # training

	print("Done training model")
	pickle.dump(clf, open(model_path, 'wb'))

	print("Saved model successfully")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
        'Train model on data')
	parser.add_argument('--file_path', type=str)
	parser.add_argument('--model_path', type=str)
	args = parser.parse_args()
	run(args)
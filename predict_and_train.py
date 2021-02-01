import argparse
import csv
import pickle
from sklearn import svm
import random

def parse_features(string_feature):
	# Take in as '[0, 0, 0, 1]' and parse into list
	list_features = string_feature[1:len(string_feature)-1]
	list_features = list_features.split(', ')
	for i in range(len(list_features)):
		list_features[i] = float(list_features[i])
	return list_features

def run(args):
	file_path = args.file_path
	trials = args.trials

	trainX = []
	trainY = []
	testX = []
	correctY = []

	data = {}
	count = 0

	with open(file_path, mode='r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			data[count] = (parse_features(row['Features']), row['Labels'])
			count += 1

	print("Done getting data")

	for j in range(trials):
		used = set()
		while len(used) < 20000:
			rand = random.randint(0, count-1)
			if rand not in used:
				trainX.append(data[rand][0])
				trainY.append(data[rand][1])
			used.add(rand)
		for i in range(count):
			if i not in used:
				testX.append(data[i][0])
				correctY.append(data[i][1])

		print("Done creating test and train datasets")

		clf = svm.SVC(kernel='linear')
		clf.fit(trainX, trainY) # training

		print("Done training model")

		testY = clf.predict(testX) # Use same feature builder and new data

		print("Done testing dataset")

		total = 0
		correct = 0
		for i in range(len(testY)):
			if testY[i] == correctY[i]:
				correct += 1
			total += 1
		print("accuracy rate for trial " + str(j) + ": " + str(correct/total))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
        'Build data file from social media posts')
	parser.add_argument('--file_path', type=str)
	parser.add_argument('--trials', type=int, default=5)
	args = parser.parse_args()
	run(args)
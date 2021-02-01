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
	geotag = args.geotag
	datapath = args.datapath
	existing_datapath = args.existing_datapath
	trained_dataset = args.trained_dataset
	write_file = args.write_file

	ids = set()
	with open(trained_dataset, mode='r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['Test Label'] != 'unrelated':
				ids.add(row['ID'])

	group_to_county = {} # facebook group name to tuple (county, state)
	with open(geotag, mode='r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['County'] != 'MANUALLY TAG':
				group_to_county[row['Name']] = (row['County'], row['State'])

	id_to_county = {} # county mapped to set of ids belonging
	with open(datapath, mode='r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['Facebook Id'] in ids:
				try:
					county = group_to_county[row['\ufeffPage Name']]
					id_to_county[row['Facebook Id']] = [county, int(row['Likes']), int(row['Comments']),
						int(row['Shares']), int(row['Love']), int(row['Wow']), int(row['Haha']),
						int(row['Sad']), int(row['Angry']), int(row['Care'])]
				except KeyError:
					continue

	id_to_data = {} # id to featurized data np array
	with open(existing_datapath, mode='r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['IDs'] in ids:
				try:
					id_to_data[row['IDs']] = parse_features(row['Features'])
					id_to_data[row['IDs']].extend(id_to_county[row['IDs']][1:])
				except KeyError:
					continue

	county_to_data = {} # county to featurized data of all 
	for (ID, info) in id_to_county.items():
		try:
			county_to_data[info[0]] = county_to_data.get(info[0], [])
			county_to_data[info[0]].extend(id_to_data[ID])
		except KeyError:
			continue

	max_size = 5643
	# Make all the same length by adding zeros
	for (county, data) in county_to_data.items():
		data.extend([0]*(max_size-len(data)))

	file = open(write_file, 'w')
	csvwriter = csv.writer(file)
	csvwriter.writerow(['Features', 'County', 'State'])

	for (county, data) in county_to_data.items():
		csvwriter.writerow([data, county[0], county[1]])



if __name__ == "__main__":
	parser = argparse.ArgumentParser(
        'Build data file from social media posts')
	parser.add_argument('--geotag', type=str, default='resources/gov_agencies_facebook_geotag.csv')
	parser.add_argument('--datapath', type=str, default='resources/2016_gov_agencies_fb.csv')
	parser.add_argument('--existing_datapath', type=str, default='social_data/2016_gov_agencies_data.csv')
	parser.add_argument('--trained_dataset', type=str, default='results/2016_gov_agencies_data.csv')
	parser.add_argument('--write_file', type=str, default='social_data/2016_gov_agencies_data_county.csv')
	args = parser.parse_args()
	run(args)
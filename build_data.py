from feature_builder import FeatureBuilder
import argparse

def run(args):
	output_file = args.output_file
	resource_file = args.resource_file
	target_file = args.target_file
	social_media_type = args.social_media_type
	model_type = args.model_type
	feature_builder = FeatureBuilder(resource_file, target_file, output_file, social_media_type, model_type) # get training data
	features = feature_builder.get_features() # may need to further flatten this out, currently 3 dimensional
	labels = [] # Get from real wtwd dataset

	# with open(self.data_path, mode='r') as csvfile:
	# 	reader = csv.DictReader(csvfile)
	# 	for row in reader:
	# 		data_point = []
	# 		if "Tag" not in row.keys():
	# 			raise LookupError("Tag of post not found")
	# 		labels.append(row["Tag"])

	# labels = np.array(labels)

	# csvfile = open(output_file, 'w') 
	# csvwriter = csv.writer(csvfile, delimiter=',')
	# csvwriter.writerow(['Features', 'Labels'])
	# csvwriter.writerow([features, labels])


	# clf = svm.SVC(kernel='linear')
	# clf.fit(features, labels) # training
	# clf.predict(test) # Use same feature builder and new data

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
        'Build data file from social media posts')
	parser.add_argument('--output_file', type=str, default='data/wtwt_data.csv')
	parser.add_argument('--resource_file', type=str, default='resources/wtwt_ids.csv')
	parser.add_argument('--target_file', type=str, default='resources/wtwt_target_words.txt')
	parser.add_argument('--social_media_type', type=str, default='twitter', choices=['twitter', 'facebook', 'instagram'])
	parser.add_argument('--model_type', type=str, default='train', choices=['train', 'test'])
	args = parser.parse_args()
	run(args)
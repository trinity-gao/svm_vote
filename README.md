# svm_vote

To use this model with other data, we need 2 groups of data: one to test on and one to train on. In this example, they are the 2016 and 2020 posts from Facebook groups, sourced from CrowdTangle. They must also be geotagged since this model will be used to predict voter turnout by county in each state. This can be done roughly using geotag_facebook.py, which crossmatches Facebook group names with a csv of groups that are already geotagged.

In general, there are two rounds of training and testing. The first is to use the wtwt dataset to tag all social media posts as support, against, unrelated, or comment. Then the second will take the 2016 social media posts and filter out the ones that were tagged as unrelated, use this to train a new model, and test this model on the 2020 dataset (also filter out unrelated posts)

Featurize the data using build_data.py, which takes in the following flags:
* --output_file: the path of the file we want to write out results to (should be csv)
* --resource_file: the path the file containing the social media posts we wants to featurize (csv, may need to check headers to match)
* --target_file: the path to the file containing target words for the code to search for (txt file, see resources/wtwt_target_words.txt for example)
* --social_media_type: either 'twitter', 'facebook', or 'instagram'
* --model_type: either 'train' or 'test'

Use predict.py to tag each of the social media posts as support, against, comment, or unrelated
* --model_path: for simplicity, use models/wtwt_model, which is trained on the Will They Won't They dataset
  * can improve here for future, using train.py with dataset other than wtwt
* --test_file: the path of the featurized data (most likely from above step) with build_data.py)

Use build_data_second.py to create our training date, with a single feature for each county in each state. This data is already crossmatched with 2020 so that counties without data from both years will be excluded. This takes all social media posts for one county and appends the features together into one feature, padding 0s so that the dimensions of each feature for each county is the same.
* --geotag: use resouces/gov_agencies_facebook_geotag.csv, which has Name, County, State has headers
* --datapath: the original csv of the social media posts sourced from CrowdTangle
* --existing_datapath: the file created by predict.py, that tags each social media post as support, against, comment or unrelated. This will be used to filter out posts that were tagged as unrelated and will not be used in creating this dataset
* --trained_dataset: the file containing Features and IDs, output from build_data.py
* --write_file: the output file of where we want to store this dataset

Use train_county.py to train the dataset on the 2016 data and create a new model. At this point, you will need the turnout rates for each county, which can be found in the voter_data folder. 
* --file_path: path to the file with one feature for each county in each state, should be the output of the last step
* --model_path: path to where you want to save the new model
* --labels_path: path to where the labels, which in this case are voter turnout, is located. In this case, requires headers state, county, and turnout_rate

Use predict_county.py to predict on 2020 data! At this point, you need to have a similar features file for 2020 as 2016, so use build_data_second.py again to featurize the according data. This will automatically write to a file in the results folder, but code can be changed to take in a flag to specify where to write to.
* --model_path: path to model we want to use, should be model built from last step
* --test_file: path to file containing features for the data we want to predict on

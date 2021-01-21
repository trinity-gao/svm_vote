import csv
import numpy as np
import argparse
import os
from subprocess import check_output
from collections import defaultdict
import re


class FeatureBuilder:

	def __init__(self, data_path, target_path, output_file, social_media_type, model_type):
		self.data_path = data_path
		self.target_path = target_path
		self.word2sentiments, self.word2emotions = self.parse_emolex()
		self.output_file = output_file
		self.social_media_type = social_media_type
		self.model_type = model_type
		self.features = self.build_features()


	def has_long(self, sentence):
	    elong = re.compile("([a-zA-Z])\\1{2,}")
	    return bool(elong.search(sentence))

	def parse_emolex(self):
		FP = 'NRC-Emotion-Lexicon/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt'
		word2sentiments = defaultdict(set)
		word2emotions = defaultdict(set)
		f = open(FP, 'r')
		for i, line in enumerate(f.readlines()):
			if i > 1:
				# line: 'abandoned\tanger\t1\n',
				word, emotion, flag = line.strip('\n').split('\t')
				if int(flag) == 1:
					if emotion == 'positive' or emotion == 'negative':
						word2sentiments[word].add(emotion)
					else:
						word2emotions[word].add(emotion)
		f.close()
		return word2sentiments, word2emotions

	def get_features(self):
		return self.features


	def get_n_grams(self, body):
		body = body.lower()
		n_grams = []

		# word 1-gram
		one_gram_word = body.split(" ")
		to_append = 1 if len(set(one_gram_word)) != len(one_gram_word) else 0
		n_grams.append(to_append)

		# word 2-gram
		two_gram_word = []
		for i in range(len(one_gram_word)-1):
			two_gram_word.append(one_gram_word[i] + " " + one_gram_word[i+1])
		to_append = 1 if len(set(two_gram_word)) != len(two_gram_word) else 0
		n_grams.append(to_append)

		# word 3-gram
		three_gram_word = []
		for i in range(len(one_gram_word)-2):
			three_gram_word.append(one_gram_word[i] + " " + one_gram_word[i+1] + " " + one_gram_word[i+2])
		to_append = 1 if len(set(three_gram_word)) != len(three_gram_word) else 0
		n_grams.append(to_append)

		chars = list(body)
		# char 2-gram
		two_gram_char = []
		for i in range(len(chars) - 1):
			two_gram_char.append(chars[i] + chars[i+1])
		to_append = 1 if len(set(two_gram_char)) != len(two_gram_char) else 0
		n_grams.append(to_append)

		# char 3-gram
		three_gram_char = []
		for i in range(len(chars) - 2):
			three_gram_char.append(chars[i] + chars[i+1] + chars[i+2])
		to_append = 1 if len(set(three_gram_char)) != len(three_gram_char) else 0
		n_grams.append(to_append)

		# char 4-gram
		four_gram_char = []
		for i in range(len(chars) - 3):
			four_gram_char.append(chars[i] + chars[i+1] + chars[i+2] + chars[i+3])
		to_append = 1 if len(set(four_gram_char)) != len(four_gram_char) else 0
		n_grams.append(to_append)

		# char 5-gram
		five_gram_char = []
		for i in range(len(chars) - 4):
			five_gram_char.append(chars[i] + chars[i+1] + chars[i+2] + chars[i+3] + chars[i+4])
		to_append = 1 if len(set(five_gram_char)) != len(five_gram_char) else 0
		n_grams.append(to_append)

		return n_grams

	def get_target(self, body, target):
		body = body.lower()
		words = body.split(" ")
		for target_word in target:
			if target_word in words:
				return [1]
		return [0]

	def get_pos(self, body):
		temp_txt = self.data_path.split(".")[0] + '.txt'
		f = open(temp_txt, "w+")
		f.write(body)
		f.read()
		out = check_output(['../ark-tweet-nlp-0.3.2/runTagger.sh', temp_txt])
		pos_types = ['N', 'O', '^', 'S', 'Z', 'V', 'A', 'R', '!', 'D', 'P', '&', 'T', 'X', '#', '@',
					 '~', 'U', 'E', '$', ',', 'G', 'L', 'M', 'Y']
		pos_types_index_dict = {}
		for i in range(len(pos_types)):
			pos_types_index_dict[pos_types[i]] = i
		pos_features = [0]*25

		out = str(out).split('\\t')
		types = out[1].split(' ')
		values = out[2].split(' ')
		for i in range(len(types)):
			pos_features[pos_types_index_dict[types[i]]] += float(values[i])
		return pos_features

	def get_sentiment(self, body):
		emotions = {'joy':0, 'trust':1, 'fear':2, 'surprise':3, 'sadness':4, 'anticipation':5, 'anger':6, 'disgust':7}
		body = body.lower()
		words = body.split(' ')
		emotions_features = [0]*8
		for word in words:
			if word in self.word2emotions:
				for emotion in self.word2emotions[word]:
					emotions_features[emotions[emotion]] += 1
		return emotions_features

	def get_encodings(self, body):
		encoding_features = [0]*7
		words = body.split(' ')
		for word in words:
			if word == '':
				continue
			else:
				# Checking for positive/negative emoticons
				if word in self.word2sentiments:
					if 'positive' in self.word2sentiments[word]:
						encoding_features[0] = 1
					if 'negative' in self.word2sentiments[word]:
						encoding_features[1] = 1
				# Checking for hashtags
				if word[0] == '#':
					encoding_features[2] = 1
				# Checking for uppercase
				if word.lower() != word:
					encoding_features[3] = 1

		# Check for elongated words
		if self.has_long(body):
			encoding_features[4] = 1

		# Check for exclamation and question marks
		chars = list(body)
		for char in chars:
			if char == '?':
				encoding_features[5] = 1
			if char == '!':
				encoding_features[6] = 1
		return encoding_features


	def build_features(self):
		features = []

		target = open(self.target_path, "r")
		target_string = target.read()
		target_array = target_string.split(", ")

		csvfile = open(self.output_file, 'a') 
		csvwriter = csv.writer(csvfile, delimiter=',')
		# if self.model_type == 'train':
		# 	csvwriter.writerow(['Features', 'Labels', 'IDs'])
		# elif self.model_type == 'test':
		# 	csvwriter.writerow(['Features', 'IDs'])

		with open(self.data_path, mode='r') as csvfile:
			reader = csv.DictReader(csvfile)
			count = 0
			for row in reader:
				count+=1
				if count > 19461:
					data_point = []
					if self.social_media_type == 'twitter':
						text_header = ["Body"]
					elif self.social_media_type =='facebook':
						text_header = ['Message', 'Image Text', 'Link Text', 'Description']
						id_header = 'Facebook Id'
					elif self.social_media_type == 'instagram':
						raise NotImplementedError("Instagram headers not implemented")

					body = ""
					for header in text_header:
						body += row[header] + " "
					media_id = row[id_header]
					# print(body)
					data_point.extend(self.get_n_grams(body))
					data_point.extend(self.get_target(body, target_array))
					data_point.extend(self.get_pos(body))
					data_point.extend(self.get_sentiment(body))
					data_point.extend(self.get_encodings(body))

					if self.model_type == 'train':
						csvwriter.writerow([data_point, row["Tag"]])
					elif self.model_type == 'test':
						csvwriter.writerow([data_point, media_id])
					print(count)
					features.append(data_point)
		return np.array(features)
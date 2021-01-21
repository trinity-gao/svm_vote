import csv
import pandas


def parse_votes(vote):
	# Turns "333,444" to 333444
	if vote == "NA":
		return 0
	else:
		return int(vote)

def parse_county(county):
	# Turn county into whatever format is expected by 2016_by_county.csv
	return county



state_county_total_vote_2016 = {}
state_county_candidate_vote_2016 = {}
state_county_candidate_winner_2016 = {}
with open('voter_data/2016_by_county_consolidated.csv', mode='rt', errors='replace') as csvfile:
	reader = csv.DictReader(csvfile)

	for row in reader:
		key = row['state'] + ',' + row['county']
		state_county_total_vote_2016[key] = row['total votes']
		state_county_candidate_vote_2016[key] = row['candidate votes']
		state_county_candidate_winner_2016[key] = row['candidate']

state_county_total_vote_2020 = {}
state_county_candidate_winner_2020 = {}
with open('voter_data/2020_by_county.csv', mode='rt', errors='replace') as csvfile:
	reader = csv.DictReader(csvfile)

	for row in reader:
		key = row['state'] + ',' + row['county']
		state_county_total_vote_2020[key] = row['total votes']
		state_county_candidate_winner_2020[key] = row['candidate']

matching_keys = set(state_county_total_vote_2016.keys()).intersection(set(state_county_total_vote_2020.keys()))
matching_keys = list(matching_keys)
matching_keys.sort()


file1 = open('voter_data/2016_cross_matched.csv', 'w')
csvwriter1 = csv.writer(file1, delimiter=',')
csvwriter1.writerow(['state', 'county', 'candidate', 'candidate votes', 'total votes'])

file2 = open('voter_data/2020_cross_matched.csv', 'w')
csvwriter2 = csv.writer(file2, delimiter=',')
csvwriter2.writerow(['state', 'county', 'candidate', 'total votes'])
for key in matching_keys:
	[state, county] = key.split(',')
	candidate1 = state_county_candidate_winner_2016[key]
	candidate_votes1 = state_county_candidate_vote_2016[key]
	total_votes1 = state_county_total_vote_2016[key]
	csvwriter1.writerow([state, county, candidate1, candidate_votes1, total_votes1])

	if state_county_candidate_winner_2020[key] == 'trump':
		candidate2 = 'Donald Trump'
	elif state_county_candidate_winner_2020[key] == 'biden':
		candidate2 = 'Joe Biden'
	else:
		candidate2 = state_county_candidate_winner_2020[key]
	total_votes2 = state_county_total_vote_2020[key]
	csvwriter2.writerow([state, county, candidate2, total_votes2])


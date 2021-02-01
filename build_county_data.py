import csv
import pandas
import xlrd

loc = 'voter_data/2010-2019_county_population.xlsx'
wb = 	xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
population_2015 = {}
population_2019 = {}
for i in range(3, 3144):
	population_2015[sheet.cell_value(i, 0).lower()] = sheet.cell_value(i, 1)
	population_2019[sheet.cell_value(i, 0).lower()] = sheet.cell_value(i, 2)

file = open('voter_data/2020_voter_data.csv', 'w')
csvwriter = csv.writer(file, delimiter=',')
csvwriter.writerow(['state', 'county', 'candidate', 'total votes', 'turnout rate'])

with open('voter_data/2020_cross_matched.csv', mode='rt', errors='replace') as csvfile:
	reader = csv.DictReader(csvfile)

	for row in reader:
		turnout_rate = None
		key = {'.' + row['county'] + ' county, ' + row['state'], '.' + row['county'] + ' city, ' + row['state'],
				'.' + row['county'] + ' parish, ' + row['state']}
		for possible_key in key:
			if possible_key in set(population_2019.keys()):
				turnout_rate = float(row['total votes'])/population_2019[possible_key]
				# print(possible_key)
				# print(float(row['total votes']))
				# print(population_2019[possible_key])
				break
		if turnout_rate == None:
			turnout_rate = "N/A"
		csvwriter.writerow([row['state'], row['county'], row['candidate'], row['total votes'], turnout_rate])

# with open('voter_data/2016_cross_matched.csv', mode='rt', errors='replace') as csvfile:
# 	reader = csv.DictReader(csvfile)
# 	keys = set()
# 	for row in reader:
# 		keys.add(row['state'] + ',' + row['county'])

# file1 = open('voter_data/2016_cross_matched_fixed.csv', 'w')
# csvwriter1 = csv.writer(file1, delimiter=',')
# csvwriter1.writerow(['state', 'county', 'candidate', 'candidate votes', 'total votes'])

# with open('voter_data/2016_consolidated_fixed.csv', mode='rt', errors='replace') as csvfile:
# 	reader = csv.DictReader(csvfile)
# 	for row in reader:
# 		if row['state'] + ',' + row['county'] in keys:
# 			csvwriter1.writerow([row['state'], row['county'], row['candidate'], row['candidate votes'], row['total votes']])
# file2 = open('voter_data/2020_voter_data.csv', 'w')
# csvwriter2 = csv.writer(file2, delimiter=',')
# csvwriter2.writerow(['state', 'county', 'candidate', 'total votes'])
# for key in matching_keys:
# 	[state, county] = key.split(',')
# 	candidate1 = state_county_candidate_winner_2016[key]
# 	candidate_votes1 = state_county_candidate_vote_2016[key]
# 	total_votes1 = state_county_total_vote_2016[key]
# 	csvwriter1.writerow([state, county, candidate1, candidate_votes1, total_votes1])

# 	if state_county_candidate_winner_2020[key] == 'trump':
# 		candidate2 = 'Donald Trump'
# 	elif state_county_candidate_winner_2020[key] == 'biden':
# 		candidate2 = 'Joe Biden'
# 	else:
# 		candidate2 = state_county_candidate_winner_2020[key]
# 	total_votes2 = state_county_total_vote_2020[key]
# 	csvwriter2.writerow([state, county, candidate2, total_votes2])

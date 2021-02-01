import csv

all_counties = set()
processed_groups = set()
matched = {}

def cross_match(page_name, county):
	# print(page_name)
	# if (county == 'houston'):
	# 	print("HERE")
	# print(county)
	words = page_name.split(' ')
	num_words = len(words)
	for i in range(num_words+1, 0, -1):
		for j in range(num_words +1 - i):
			words_to_consider = ""
			for k in range(j, j+i, 1):
				if k < j+i-1:
					words_to_consider += words[k].lower() + ' '
				else:
					words_to_consider += words[k].lower()
			# print(words_to_consider)
			if words_to_consider == county:
				return True
	return False


with open('voter_data/2016_voter_data.csv', mode='rt', errors='replace') as csvfile:
	reader = csv.DictReader(csvfile)

	for row in reader:
		all_counties.add((row['county'], row['state']))

with open('resources/gov_agencies_facebook_geotag.csv', mode='rt', errors='replace') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		processed_groups.add(row['Name'])


file = open('resources/gov_agencies_facebook_geotag.csv', 'a')
csvwriter = csv.writer(file, delimiter=',')

with open('resources/2016_gov_agencies_fb.csv') as csvfile:
	reader = csv.DictReader(csvfile)

	for row in reader:
		# break;
		if row['\ufeffPage Name'] not in processed_groups:
			for county in all_counties:
				# print(cross_match(row['\ufeffGroup Name'], county[0]))

				if cross_match(row['\ufeffPage Name'], county[0]):
					# if row['\ufeffPage Name'] in matched.keys():
					# 	matched[row['\ufeffPage Name']] = "MANUALLY TAG"
					# else:
					matched[row['\ufeffPage Name']] = county
			if (row['\ufeffPage Name']) not in matched.keys():
				matched[row['\ufeffPage Name']] = "MANUALLY TAG"
			processed_groups.add(row['\ufeffPage Name'])
for (page_name, county) in matched.items():
	if county == 'MANUALLY TAG':
		csvwriter.writerow([page_name, county])
	else:
		csvwriter.writerow([page_name, county[0], county[1]])
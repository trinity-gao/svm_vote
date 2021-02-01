import csv
import math

predicted_turnout = {}
actual_turnout = {}

def parse(county):
	county = county[1:len(county)-1]
	county = county.split(',')
	return (county[0][1:len(county[0])-1], county[1][2:len(county[1])-1])

with open('results/2020_gov_agencies_data_county.csv', mode='r') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if row['Predicted Turnout'] != "N/A":
			predicted_turnout[parse(row['County'])] = float(row['Predicted Turnout'])

with open('voter_data/2020_voter_data.csv', mode='r') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		# print((row['county'], row['state']))
		# print(predicted_turnout.keys())
		if (row['county'], row['state']) in predicted_turnout.keys() and row['turnout rate'] != 'N/A':
			actual_turnout[(row['county'], row['state'])] = float(row['turnout rate'])


total_error = 0
count = 0
not_found_count = 0
number_within_epsilon1 = 0
number_within_epsilon2 = 0
number_within_epsilon3 = 0
epsilon1 = 0.05
epsilon2 = 0.10
epsilon3 = 0.15
for county in predicted_turnout.keys():
	try:
		total_error += abs(predicted_turnout[county] - actual_turnout[county])
		if abs(predicted_turnout[county] - actual_turnout[county]) <= epsilon1:
			number_within_epsilon1 += 1
		if abs(predicted_turnout[county] - actual_turnout[county]) <= epsilon2:
			number_within_epsilon2 += 1
		if abs(predicted_turnout[county] - actual_turnout[county]) <= epsilon3:
			number_within_epsilon3 += 1
		count += 1
	except KeyError:
		not_found_count += 1

print("average difference in turnout rate across " + str(count) + " counties: " + str(total_error/count))
print("number of counties within " + str(epsilon1) + " of actual turnout: " + str(number_within_epsilon1) + 
	" out of " + str(count) + " counties for a ratio of " + str(number_within_epsilon1/count))
print("number of counties within " + str(epsilon2) + " of actual turnout: " + str(number_within_epsilon2) + 
	" out of " + str(count) + " counties for a ratio of " + str(number_within_epsilon2/count))
print("number of counties within " + str(epsilon3) + " of actual turnout: " + str(number_within_epsilon3)+ 
	" out of " + str(count) + " counties for a ratio of " + str(number_within_epsilon3/count))
print(str(not_found_count) + " counties have no voting data")


from __future__ import print_function
import math
pairs={}

with open("data/result_info.csv", 'r') as my_csv_file:
	for line in my_csv_file:
		line=line.split(',')
		if not line[1]: #if not full
			continue
		destination = line[3]
		probe = line[2]
		dest_reached = line[6]
		if not destination in pairs.keys(): #if destination not seen
			if dest_reached=='True':
				pairs[destination]={probe:[1,1]}
			else:
				pairs[destination]={probe:[0,1]}
		elif not probe in pairs[destination].keys(): #if destination seen but probe not seen
			if dest_reached=='True':
				pairs[destination][probe]=[1,1]
			else:
				pairs[destination][probe]=[0,1]
		else: #entire probe, destination pair has been seen already
			if dest_reached=='True':
				pairs[destination][probe][0]+=1
			pairs[destination][probe][1]+=1
#print pairs

percents = []
for destination in pairs.keys():
	for probe in pairs[destination].keys():
		percent_reached = pairs[destination][probe][0]*100/pairs[destination][probe][1]
		percents.append(percent_reached)
		print(percent_reached, end=", ")
print()
mean = 0
for percent in percents:
	mean += percent
mean = mean/len(percents)
print(mean)

std_dev = 0
for percent in percents:
	std_dev += ((percent-mean)*(percent-mean))
std_dev = math.sqrt(std_dev/len(percents))
print(std_dev)

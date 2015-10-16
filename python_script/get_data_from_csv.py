from __future__ import print_function
import math
pairs={}

with open("data/result_info.csv", 'r') as my_csv_file:
	for line in my_csv_file:
		line=line.split(',')
		if not line[1]=="True": #if not full
			continue
		destination = line[3]
		probe = line[2]
		dest_reached = line[6]

		#looking at full path to see if different
		hops = line[-1]

		if not destination in pairs.keys(): #if destination not seen
			if dest_reached=='True':
				pairs[destination]={probe:[[1,1],[hops]]}
			else:
				pairs[destination]={probe:[[0,1],[hops]]}
		elif not probe in pairs[destination].keys(): #if destination seen but probe not seen
			if dest_reached=='True':
				pairs[destination][probe]=[[1,1],[hops]]
			else:
				pairs[destination][probe]=[[0,1],[hops]]
		else: #entire probe, destination pair has been seen already
			if dest_reached=='True':
				pairs[destination][probe][0][0]+=1
			pairs[destination][probe][0][1]+=1
			pairs[destination][probe][1].append(hops)

#find mean and standard deviation
percents = []
for destination in pairs.keys():
	for probe in pairs[destination].keys():
		percent_reached = pairs[destination][probe][0][0]*100/pairs[destination][probe][0][1]
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

#check to see how many paths are different per pair
diff_paths = []
for destination in pairs.keys():
	for probe in pairs[destination].keys():
		all_paths = []
		for path in pairs[destination][probe][1]:
			if path in all_paths:
				continue
			else:
				all_paths.append(path)
		diff_outof_all = len(all_paths)*100/pairs[destination][probe][0][1]
		diff_paths.append(diff_outof_all)

mean = 0
for diff_path in diff_paths:
	mean += diff_path
mean = mean/len(diff_paths)
print(mean)

std_dev = 0
for diff_path in diff_paths:
	std_dev += ((diff_path-mean)*(diff_path-mean))
std_dev = math.sqrt(std_dev/len(diff_paths))
print(std_dev)

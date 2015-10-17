from __future__ import print_function
import math

def print_mean_and_std_dev(array):
    mean=0
    for el in array:
        mean += el
    mean = mean/len(array)
    print(mean)

    std_dev = 0
    for el in array:
        std_dev += ((el-mean)*(el-mean))
    std_dev = math.sqrt(std_dev/len(array))
    print(std_dev)

pairs={}

with open("data/result_info.csv", 'r') as my_csv_file:
	for line in my_csv_file:
		line=line.split(',')
		if not line[1]=="True": #if not full
			continue
		destination = line[3]
		probe = line[2]
		dest_reached = line[6]
		proto = line[5]

		#looking at full path to see if different
		hops = line[-1]

		if not destination in pairs.keys(): #if destination not seen
			if dest_reached=='True':
				pairs[destination]={probe:[[1,1],[hops],[proto]]}
			else:0
				pairs[destination]={probe:[[0,1],[hops],[proto]]}
		elif not probe in pairs[destination].keys(): #if destination seen but probe not seen
			if dest_reached=='True':
				pairs[destination][probe]=[[1,1],[hops],[proto]]
			else:
				pairs[destination][probe]=[[0,1],[hops],[proto]]
		else: #entire probe, destination pair has been seen already
			if dest_reached=='True':
				pairs[destination][probe][0][0]+=1
			pairs[destination][probe][0][1]+=1
			pairs[destination][probe][1].append(hops)
			pairs[destination][probe][2].append(proto)

#find mean and standard deviation
percents = []
diff_paths = []
for destination in pairs.keys():
    for probe in pairs[destination].keys():
        #check to see how many paths are different per pair
        all_paths = []
        for path in pairs[destination][probe][1]:
            if path in all_paths:
                continue
            else:
                all_paths.append(path)
        diff_outof_all = len(all_paths)*100/pairs[destination][probe][0][1]
        diff_paths.append(diff_outof_all)
        #percent reached
        percent_reached = pairs[destination][probe][0][0]*100/pairs[destination][probe][0][1]
        percents.append(percent_reached)

#mean and std dev for percent of paths which reached destination for each probe,destination pair
print_mean_and_std_dev(percents)
#mean and std_dev for percent of paths that were different
print_mean_and_std_dev(diff_paths)

#does the change of path correlate with the change of protocol?

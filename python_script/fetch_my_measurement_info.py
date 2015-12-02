from subprocess import call
import sys
import os

folder = sys.argv[1]
percent = 0
count=0
num_files = len(os.listdir(folder))
for filename in os.listdir(folder):
    count+=1
    if not percent == int((count*100)//num_files):
        print(percent)
    percent = int((count*100)//num_files)

    filename = folder+'/'+filename
    measure_id_file = open(filename, 'r')
    measure_ids = measure_id_file.readlines()
    measure_id_file.close()
    for measure_id in measure_ids:
        link = "https://atlas.ripe.net/api/v1/measurement/"+measure_id.strip()+"/?fields="
        name = "results/measurement_info/info_for_"+measure_id.strip()+".json"
        myfile = open(name, 'w')
        call(["curl", link], stdout=myfile) #to results file depending on measure_id
        myfile.close()

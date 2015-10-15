from subprocess import call
import sys
import os

#usage to make sure correct arguments supplied
if len(sys.argv)!=2:
    print("specify python file and location of measurement ids\neg: python fetch_results.py measure_ids.txt")
    sys.exit(1)

folder = sys.argv[1]
#percent = 0
count = 1
tot = len(os.listdir(folder))
for filename in os.listdir(folder):
    #if not percent==int((count*100)//tot):
    print((count*100)/tot)
    #percent=int((count*100)//tot)
    count+=1
    filename = folder+'/'+filename
    measure_id_file = open(filename, 'r')
    measure_ids = measure_id_file.readlines()
    measure_id_file.close()
    for measure_id in measure_ids:
        link = "https://atlas.ripe.net/api/v1/measurement/"+measure_id.strip()+"/result/?key=13161419-65ad-4c40-92c8-0cd8a22a2ab2"
        name = "results/result_for_"+measure_id.strip()+".json"
        myfile = open(name, 'w')
        call(["curl", link], stdout=myfile) #to results file depending on measure_id
        myfile.close()

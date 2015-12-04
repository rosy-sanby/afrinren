import sys
from subprocess import call
import os


folder = "measurements_partial/"
idnum=1

percent = 1
total = 1800
for filename in os.listdir(folder):
    protocol = filename[:filename.find('_')]
    
    with open(folder+"/"+filename, 'r') as lines:
        for line in lines.readlines():
            print(int(percent*100/1800))
            percent+=1
            info = line.split(' ')
            probe = info[1]
            dst_addr = info[2]
            alter = info[3].split(',')
            firsthop = alter[0][1:]
            maxhops = alter[1][:-2]
            with open("new_measurement", 'w') as new_one:
                new_one.write(dst_addr+' '+probe)
            path = "new_measurement"
            
            with open("measurements_done_"+protocol+"_partial", 'r') as done:
                if dst_addr+' '+probe+'\n' in done.readlines():
                    print("done already")
                    continue
            description = "Traceroute"+str(idnum)+" "+protocol+" from "+probe+" to "+dst_addr+" (partial)"
            
            measure_id_path = "atlas/measure_ids/partial_measurements/measure_ids_"+protocol+"_"+probe+"_to_"+dst_addr+"_"+str(idnum)+".txt" 
            call(['python', 'atlas/atlas_traceroute.py', '-d', description, '-k', 'data/api_key_1', '-p', protocol, '--firsthop', firsthop, '--maxhops', maxhops, path, measure_id_path])
            with open("measurements_done_"+protocol+"_partial",'a') as done:
                done.write(dst_addr+' '+probe+'\n')
            idnum+=1



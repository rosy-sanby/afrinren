import sys
from subprocess import call
import os

folder = sys.argv[1]
protocol = sys.argv[2]

if len(sys.argv)<4:
    for filename in os.listdir(folder):
        path = folder+filename
        with open("measurements_done_"+protocol, 'r') as done:
            if path+'\n' in done.readlines():
                print("done already")
                continue
        #k = filename.rfind("_")
       # number = filename[k+1:-4].strip()
#        if not (number=="29" or number=="37"):
 #           print("Number is: "+number)
  #          continue
        #print(number)    
        #description = "Traceroute "+protocol+" and paris 0: "+str(number)
        description = "Traceroute "+protocol+" from "+filename[filename.rfind('_')+1:filename.rfind('.')]+" to "+filename[filename.find('_')+1:filename[filename.find('_')+1:].find('_')+filename.find('_')+1]+" (as is)"        
        
        #start_time = "1444165200"
        #measure_id_path = "atlas/measure_ids/new_set/measure_ids_"+protocol+"_oneoff_"+str(number)+".txt"
        measure_id_path = "atlas/measure_ids/new_set_2_overlaps/measure_ids_"+protocol+"_"+filename[filename.rfind('_')+1:filename.rfind('.')]+"_to_"+filename[filename.find('_')+1:filename[filename.find('_')+1:].find('_')+filename.find('_')+1]+".txt" 
        print(path)       
        call(['python', 'atlas/atlas_traceroute.py', '-d', description, '-k', 'data/api_key_1', '-p', protocol, path, measure_id_path])
        with open("measurements_done_"+protocol,'a') as done:
            done.write(path+'\n')
        #break
    
else:
    paris = sys.argv[3]
    for filename in os.listdir(folder):
        k = filename.rfind("_")
        number = filename[k+1:-4]
        print(number)
        #if number=="40" or number=="29": 
            #continue
        description = "Traceroute "+protocol+" and paris "+paris+": "+str(number)
        path = folder+filename
        measure_id_path = "atlas/measure_ids/paris0/measure_ids_"+protocol+"_oneoff_"+str(number)+".txt"
        call(['sudo','python', 'atlas/atlas_traceroute.py', '-d', description, '-k', 'data/api_key_1', '-p', protocol, '--paris', paris, path, measure_id_path])
        #break

import sys
from subprocess import call
import os

folder = sys.argv[1]
protocol = sys.argv[2]

if len(sys.argv)<4:
    for filename in os.listdir(folder):
        k = filename.rfind("_")
        number = filename[k+1:-4].strip()
#        if not (number=="29" or number=="37"):
 #           print("Number is: "+number)
  #          continue
        print(number)    
        description = "Traceroute "+protocol+" and paris 0: "+str(number)
        path = folder+filename
        measure_id_path = "atlas/measure_ids/paris0/measure_ids_"+protocol+"_oneoff_"+str(number)+".txt"
        call(['sudo','python', 'atlas/atlas_traceroute.py', '-d', description, '-k', 'data/api_key_1', '-p', protocol, path, measure_id_path])
        #break
    
else:
    paris = sys.argv[3]
    for filename in os.listdir(folder):
        k = filename.rfind("_")
        number = filename[k+1:-4]
        print(number)
        if int(number)==29: 
            continue
        description = "Traceroute "+protocol+" and paris "+paris+": "+str(number)
        path = folder+filename
        measure_id_path = "atlas/measure_ids/paris0/measure_ids_"+protocol+"_oneoff_"+str(number)+".txt"
        call(['sudo','python', 'atlas/atlas_traceroute.py', '-d', description, '-k', 'data/api_key_1', '-p', protocol, '--paris', paris, path, measure_id_path])
        break

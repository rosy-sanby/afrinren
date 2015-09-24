import sys
from subprocess import call
import os

folder = sys.argv[1]
protocol = sys.argv[2]

for filename in os.listdir(folder):
    k = filename.rfind("_")
    number = filename[k+1:-4]
    print(number)
    description = "Traceroute "+protocol+" one-off and paris 0 "+str(number)
    path = folder+filename
    measure_id_path = "atlas/measure_ids/newest/measure_ids_"+protocol+"_oneoff_"+str(number)+".txt"
    call(['python', 'atlas/atlas_traceroute.py', '-d', description, '-k', 'data/api_key_1', '-p', protocol, '--paris', '0' path, measure_id_path])

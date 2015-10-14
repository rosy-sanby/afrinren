import sys
from subprocess import call
import os

print("----------------------------------------------FULL ONES----------------------------------------------------------")

folder = "full_measurements/"
protocols = ["ICMP","TCP","UDP"]
idnum=2001
number=0
while number<1:
    for protocol in protocols:
        for filename in os.listdir(folder):
            path = folder+filename
            with open("measurements_done_"+protocol+"_full", 'r') as done:
                if path+'\n' in done.readlines():
                    print("done already")
                    continue
            description = "Traceroute"+str(idnum)+" "+protocol+" from "+filename[filename.rfind('_')+1:filename.rfind('.')]+" to "+filename[filename.find('_')+1:filename[filename.find('_')+1:].find('_')+filename.find('_')+1]+" (full)"        
            
            measure_id_path = "atlas/measure_ids/new_measurements/measure_ids_"+protocol+"_"+filename[filename.rfind('_')+1:filename.rfind('.')]+"_to_"+filename[filename.find('_')+1:filename[filename.find('_')+1:].find('_')+filename.find('_')+1]+"_"+str(idnum)+".txt" 
            print(path)       
            call(['sudo','python', 'atlas/atlas_traceroute.py', '-d', description, '-k', 'data/api_key_1', '-p', protocol, path, measure_id_path])
            with open("measurements_done_"+protocol+"_full",'a') as done:
                done.write(path+'\n')
            idnum+=1
    number+=1
        #break

print("----------------------------------------------DOING OVERLAPPED ONES----------------------------------------------------------")
folder = "measurements/"
for protocol in protocols:    
    with open("data/new_measurements_with_overlaps_"+protocol, 'r') as overlaps:
        lines = overlaps.readlines()

    prev_dest=""
    count=1
    for line in lines:
        overlap = line.split(' ') #0probe | 1dst_addr | 2firsthop | 3dst | 4new_dst_addr | 5prb
        path = folder+"target_"+overlap[1]+"_and_probe_"+overlap[0]+".txt"
        if overlap[4] == prev_dest:
            count+=1
            #print(count)
        else:
            count=1
        if count>=10:
            continue
        prev_dest=overlap[4]
        with open("measurements_done_"+protocol, 'r') as done:
            if path+'\n' in done.readlines():
                print("done already")
                continue
        if not overlap[4][:overlap[4].find('.')]=="10" and not overlap[4][:overlap[4].find('.')]=="172" and not overlap[4][:overlap[4][overlap[4].find('.')+1:].find('.')+overlap[4].find('.')+1]=="192.168": #check that this is a public address
            with open(path, 'w') as target_and_prb:
                target_and_prb.write(overlap[4]+" "+overlap[0])
        
        description = "Traceroute"+str(idnum)+" "+protocol+" from "+overlap[0]+" to "+overlap[1]+" ("+overlap[3]+","+overlap[5]+")"
        measure_id_path = "atlas/measure_ids/new_measurements_overlap/measure_ids_"+protocol+"_"+overlap[0]+"_to_"+overlap[1]+"_"+str(idnum)+".txt"
        idnum+=1
        firsthop = overlap[2]
        try:    
            call(['sudo', 'python', 'atlas/atlas_traceroute.py', '-d', description, '-k', 'data/api_key_1', '-p', protocol, '--firsthop', firsthop, path, measure_id_path])
            with open("measurements_done_"+protocol,'a') as done:
                done.write(path+'\n')
        except:
            with open ("to_redo", 'a') as redo:
                redo.write("REDO: "+protocol+" "+path+'\n')
            continue
 
print("----------------------------------------------REDOING MISSED ONES----------------------------------------------------------")
for protocol in protocols:    
    with open("data/new_measurements_with_overlaps_"+protocol, 'r') as overlaps:
        lines = overlaps.readlines()

    prev_dest=""
    count=1
    for line in lines:
        overlap = line.split(' ') #0probe | 1dst_addr | 2firsthop | 3dst | 4new_dst_addr | 5prb
        path = folder+"target_"+overlap[1]+"_and_probe_"+overlap[0]+".txt"
        if overlap[4] == prev_dest:
            count+=1
            #print(count)
        else:
            count=1
        if count>=10:
            continue
        prev_dest=overlap[4]
        with open("measurements_done_"+protocol, 'r') as done:
            if path+'\n' in done.readlines():
                print("done already")
                continue
        if not overlap[4][:overlap[4].find('.')]=="10" and not overlap[4][:overlap[4].find('.')]=="172" and not overlap[4][:overlap[4][overlap[4].find('.')+1:].find('.')+overlap[4].find('.')+1]=="192.168": #check that this is a public address
            with open(path, 'w') as target_and_prb:
                target_and_prb.write(overlap[4]+" "+overlap[0])
        
        description = "Traceroute"+str(idnum)+" "+protocol+" from "+overlap[0]+" to "+overlap[1]+" ("+overlap[3]+","+overlap[5]+")"
        measure_id_path = "atlas/measure_ids/new_measurements_overlap/measure_ids_"+protocol+"_"+overlap[0]+"_to_"+overlap[1]+"_"+str(idnum)+".txt"
        idnum+=1
        firsthop = overlap[2]
        try:    
            call(['sudo', 'python', 'atlas/atlas_traceroute.py', '-d', description, '-k', 'data/api_key_1', '-p', protocol, '--firsthop', firsthop, path, measure_id_path])
            with open("measurements_done_"+protocol,'a') as done:
                done.write(path+'\n')
        except:
            with open ("to_redo", 'a') as redo:
                redo.write("REDO: "+protocol+" "+path+'\n')
            continue

print("----------------------------------------------FINISHING OFF OVERLAPPED ONES----------------------------------------------------------")

for protocol in protocols:
    for filename in os.listdir(folder):
        path = folder+filename
        with open("measurements_done_"+protocol, 'r') as done:
            if path+'\n' in done.readlines():
                print("done already")
                continue
        description = "Traceroute"+str(idnum)+" "+protocol+" from "+filename[filename.rfind('_')+1:filename.rfind('.')]+" to "+filename[filename.find('_')+1:filename[filename.find('_')+1:].find('_')+filename.find('_')+1]+" (as is)"        
        
        measure_id_path = "atlas/measure_ids/new_measurements_overlap/measure_ids_"+protocol+"_"+filename[filename.rfind('_')+1:filename.rfind('.')]+"_to_"+filename[filename.find('_')+1:filename[filename.find('_')+1:].find('_')+filename.find('_')+1]+"_"+str(idnum)+".txt" 
        print(path)       
        call(['sudo', 'python', 'atlas/atlas_traceroute.py', '-d', description, '-k', 'data/api_key_1', '-p', protocol, path, measure_id_path])
        with open("measurements_done_"+protocol,'a') as done:
            done.write(path+'\n')
        idnum+=1


#else:
 #   paris = sys.argv[3]
  #  for filename in os.listdir(folder):
   #     k = filename.rfind("_")
    #    number = filename[k+1:-4]
     #   print(number)
        #if number=="40" or number=="29": 
            #continue
 #       description = "Traceroute "+protocol+" and paris "+paris+": "+str(number)
  #      path = folder+filename
   #     measure_id_path = "atlas/measure_ids/paris0/measure_ids_"+protocol+"_oneoff_"+str(number)+".txt"
    #    call(['sudo','python', 'atlas/atlas_traceroute.py', '-d', description, '-k', 'data/api_key_1', '-p', protocol, '--paris', paris, path, measure_id_path])
        #break

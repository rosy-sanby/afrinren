protocol = "TCP"

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
    with open("measurements_done_TCP", 'r') as done:
        if path+'\n' in done.readlines():
            print("done already")
            continue
    if not overlap[4][:overlap[4].find('.')]=="10" and not overlap[4][:overlap[4].find('.')]=="172" and not overlap[4][:overlap[4][overlap[4].find('.')+1:].find('.')+overlap[4].find('.')+1]=="192.168": #check that this is a public address
        with open(path, 'w') as target_and_prb:
            target_and_prb.write(overlap[4]+" "+overlap[0])
    
    description = "Traceroute2 "+protocol+" from "+overlap[0]+" to "+overlap[1]+" ("+overlap[3]+","+overlap[5]+")"
    measure_id_path = "atlas/measure_ids/new_set_2_overlaps/measure_ids_"+protocol+"_"+overlap[0]+"_to_"+overlap[1]+".txt"
    firsthop = overlap[2]
    try:
        call(['python', 'atlas/atlas_traceroute.py', '-d', description, '-k', 'data/api_key_1', '-p', protocol, '--firsthop', firsthop, path, measure_id_path])
        with open("measurements_done_TCP",'a') as done:
            done.write(path+'\n')
    except:
        print("REDO: "+protocol+" "+path)
        continue
    
protocol = "UDP"

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
    with open("measurements_done_UDP", 'r') as done:
        if path+'\n' in done.readlines():
            print("done already")
            continue
    if not overlap[4][:overlap[4].find('.')]=="10" and not overlap[4][:overlap[4].find('.')]=="172" and not overlap[4][:overlap[4][overlap[4].find('.')+1:].find('.')+overlap[4].find('.')+1]=="192.168": #check that this is a public address
        with open(path, 'w') as target_and_prb:
            target_and_prb.write(overlap[4]+" "+overlap[0])
    
    description = "Traceroute2 "+protocol+" from "+overlap[0]+" to "+overlap[1]+" ("+overlap[3]+","+overlap[5]+")"
    measure_id_path = "atlas/measure_ids/new_set_2_overlaps/measure_ids_"+protocol+"_"+overlap[0]+"_to_"+overlap[1]+".txt"
    firsthop = overlap[2]
    try:
        call(['python', 'atlas/atlas_traceroute.py', '-d', description, '-k', 'data/api_key_1', '-p', protocol, '--firsthop', firsthop, path, measure_id_path])
        with open("measurements_done_UDP",'a') as done:
            done.write(path+'\n')
    except:
        print("REDO: "+protocol+" "+path)
        continue

from __future__ import print_function
import os
import sys
import json

folder = sys.argv[1] #results/json/
number = 1

csv_file = open("data/result_info.csv", 'w')

result_info = ["id", "full", "probe", "dest", "dest_sent_to", "protocol", "dest_reached", "somewhere_reached", "first_hop", "num_hops", "num_x_hops", "latency", "avg_rtt", "hops"]

for info in result_info:
    csv_file.write(str(info)+',')
#        csv_file.write(',')
csv_file.write('\n')

for filename in os.listdir(folder):
    if not filename[-5:] == ".json":
        continue
    with open(folder+filename, 'r') as my_file: 
        results = json.load(my_file)
    filename = filename.split('_') #protocol_to_dest(measureid).json
    
    measurement_id = filename[2][filename[2].find('(')+1:filename[2].find(')')]
    
    try:
        #open measurement info
        with open("results/measurement_info/info_for_"+measurement_id.strip()+".json",'r') as my_info_file:
            my_info = json.load(my_info_file)
            #print(measurement_id, end=": ")
            description = my_info['description']
            
            if description.split(' ')[2]=="from":
                dest = description[description.find("to")+3:description.find("(")-1]
                if dest == "and":
                    dest=False
                dest_sent_to = my_info['dst_name']
                if description[description.find('(')+1:description.find(')')] == "full":
                    full = True
                else:
                    full = False
            else:
                dest = False
                full =True

            #get ref buddies
            if len(description.split(' '))<=6 or (description.split(' ')[6]=="(as" or full):
                ref = None
            else: #ref is [probe buddy(diff dst, same probe), dst buddy(diff probe, same dest)]
                ref = [description.split(' ')[6].split(',')[0].strip()[1:], description.split(' ')[6].split(',')[1].strip()[:-1]]
                
    except IOError:
        #if not full:
        dest = filename[2][:filename[2].find('(')]+"?" #the ip address it was actually sent to (not necessarily target)
        #else:
         #   dest = filename[2][:filename[2].find('(')]
        dest_sent_to = dest
        ref = None
        full = True
    
    protocol = filename[0]
          
    for result in results:
        result_info = [] #[measurement_id(int), probe(int), dest(str), dest_sent_to(str), protocol(str), 
                        #dest_reached(bool), somewhere_reached(bool), first_hop(int), num_hops(int), 
                        #num_x_hops(int), latency(int), avg_rtt(int), full(bool)]
        result_info.append(measurement_id)
        result_info.append(full)
        probe = result['prb_id']
        latency = result['latency']
        if not dest:
            dest = result['dst_name']
            dest_sent_to = result['dst_name']
        #find buddies
        probe_buddy={}
        dest_buddy={}
        if ref:
            for json_file in os.listdir("results/json/"):
                if json_file[:json_file.find('(')]==protocol+"_to_"+dest and int(json_file[json_file.find('(')+1:json_file.find(')')])<2487080: #this number should work as overlaps were based on these measurements
                    with open("results/json/"+json_file, 'r') as full_trace:
                        my_full_trace = json.load(full_trace)
                    for trace in my_full_trace:
                        if trace.has_key("prb_id") and int(trace["prb_id"])==int(ref[1]):
                            dest_buddy=trace
                            break
                #find dest buddy measurement        
                elif json_file[:json_file.find('(')]==protocol+"_to_"+ref[0] and int(json_file[json_file.find('(')+1:json_file.find(')')])<2487080:
                    with open("results/json/"+json_file, 'r') as buddy_file:
                        my_buddy_trace = json.load(buddy_file)
                    for trace in my_buddy_trace:
                        if trace.has_key("prb_id") and int(trace["prb_id"])==int(probe):
                            probe_buddy=trace
                            break
        
        hops=[]
        dest_reached = False
        somewhere_reached = True
        num_hops = 0
        num_x_hops = 0
        avg_rtt = 0
        count = 1
        first_hop = 1
        
        for hop in result['result']:
           
            if hop['hop'] >= 255:
                num_hops += 1
                somewhere_reached = False
            else:
                if count == 1:
                    first_hop = hop['hop']
                    count+=1 
                    #print(full)
                    #print(hop['hop'])
                    #add on beginning section
                    if not full and ref and probe_buddy:
                        same_found = False
                        for info in probe_buddy['result']:
                            if info['result'].has_key('from'):
                                if  hop['result'].has_key('from') and info['result']['from'] == hop ['result']['from']:
                                    same_found = True
                                    break
                                else:
                                    hops.append(info['result']['from'])
                            elif not same_found:
                                hops.append(info['result']['x'])
                num_hops += 1
                if hop['result'].has_key('rtt'):
                    avg_rtt += hop['result']['rtt']
            if hop['result'].has_key('x'):
                hops.append(hop['result']['x'])
                num_x_hops += 1
            elif hop['result']['from'] == dest:
                dest_reached = True
                hops.append(dest)
            elif hop['result']['from'] == dest_sent_to: #add on end section
                if not full and ref and dest_buddy:
                    same_found = False
                    for info in dest_buddy['result']:
                        if info['result'].has_key('from'):
                            if info['result']['from'] == hop ['result']['from']:
                                same_found = True
                            if not same_found:
                                continue
                            else:
                                hops.append(info['result']['from'])
                        elif same_found:
                            hops.append(info['result']['x']) 
                    if same_found and hops[-1] == dest:
                        dest_reached = True
                    break
            else:
                hops.append(hop['result']['from'])
        if (num_hops - num_x_hops)>0:
            avg_rtt = avg_rtt / (num_hops - num_x_hops)
        else:
            avg_rtt = 0
    
        result_info.append(probe)
        result_info.append(dest)
        result_info.append(dest_sent_to)
        result_info.append(protocol)
        result_info.append(dest_reached)
        result_info.append(somewhere_reached)
        result_info.append(first_hop)
        result_info.append(num_hops)
        result_info.append(num_x_hops)
        result_info.append(latency)
        result_info.append(avg_rtt)
        
        for info in result_info:
            csv_file.write(str(info)+',')
    #        csv_file.write(',')
        for hop in hops:
            csv_file.write(hop+';')
        csv_file.write('\n')
        print(number)
        number+=1
    
csv_file.close()

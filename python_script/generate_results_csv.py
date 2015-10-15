from __future__ import print_function
import os
import sys
import json

folder = sys.argv[1] #results/json/

csv_file = open("data/result_info.csv", 'w')

result_info = ["id", "full", "probe", "dest", "dest_sent_to", "protocol", "dest_reached", "somewhere_reached", "first_hop", "num_hops", "num_x_hops", "latency", "avg_rtt", "hops"]

for info in result_info:
    csv_file.write(str(info)+',')
#        csv_file.write(',')
csv_file.write('\n')
lowest=99999999
for filename in os.listdir(folder):
    if not filename[-5:] == ".json":
        continue
    with open(folder+filename, 'r') as my_file: 
        results = json.load(my_file)
    filename = filename.split('_') #protocol_to_dest(measureid).json
    
    measurement_id = filename[2][filename[2].find('(')+1:filename[2].find(')')]
    #if int(measurement_id)>2487080:
     #   full = False
    #else:
       # full = True
     #   continue
    if int(measurement_id)<lowest:
        lowest = int(measurement_id)
#    print(measurement_id)
    
    try:
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
    except IOError:
        #if not full:
        dest = filename[2][:filename[2].find('(')]+"?" #the ip address it was actually sent to (not necessarily target)
        #else:
         #   dest = filename[2][:filename[2].find('(')]
        dest_sent_to = dest
    protocol = filename[0]
    
    for result in results:
        result_info = [] #[measurement_id(int), probe(int), dest(str), dest_sent_to(str), protocol(str), 
                        #dest_reached(bool), somewhere_reached(bool), first_hop(int), num_hops(int), 
                        #num_x_hops(int), latency(int), avg_rtt(int), full(bool)]
        result_info.append(measurement_id)
        result_info.append(full)
        probe = result['prb_id']
        latency = result['latency']
        hops=[]
        if not dest:
            dest = result['dst_name']
            dest_sent_to = result['dst_name']
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
                num_hops += 1
                if hop['result'].has_key('rtt'):
                    avg_rtt += hop['result']['rtt']
            if hop['result'].has_key('x'):
                num_x_hops += 1
            elif hop['result']['from'] == dest:
                dest_reached = True
                hops.append(dest)
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
    
csv_file.close()
print(lowest)

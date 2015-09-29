#working with already aggregated/summarised data
from __future__ import print_function
import sys
import os
import json

folder = sys.argv[1] # in general results/json

#put traceroutes to same destination together in a dictionary {ip_address: [filename_1, filename_2, filename_3]}
traceroutes = {}
probe_ids = {}
protocols = {}
reached_dest = {}
reached_somewhere = {}
latency = {}
num_hops = {}
num_x_hops = {}
num_consec_hops = {}
for filename in os.listdir(folder):
    if filename[-5:]!=".json":
        continue
    k=filename[:filename[:filename.rfind("_")-1].rfind("_")].rfind("_")
    number = int(filename[k+1:filename[:filename.rfind("_")-1].rfind("_")])
    #print(number)
    if number<2439524 or (number<2457306 and number>2456864):
        continue
    
    json_data = open(folder+"/"+filename,'r')
    json_info = json.load(json_data)
    json_data.close()

    dst_addr = json_info[0]["dst_addr"]
    if not dst_addr in traceroutes:
        traceroutes[dst_addr] = [number]
    else:
        traceroutes[dst_addr].append(number)
   
    protocols[number] = json_info[0]["proto"]
    reached_dest[number] = {}
    reached_somewhere[number] = {}
    latency[number] = {}
    num_hops[number] = {}
    num_x_hops[number] = {}
    probe_ids[dst_addr]=[]
    num_consec_hops[number] = {}
    
    for result in json_info:
        prb_id = result["prb_id"]
#.....
        if not dst_addr in probe_ids:
            probe_ids[dst_addr] = [prb_id]
        elif not prb_id in probe_ids[dst_addr]:
            probe_ids[dst_addr].append(prb_id)
        reached_dest[number][result["prb_id"]] = False    
        reached_somewhere[number][prb_id] = True
        latency[number][prb_id] = str(result["latency"])
        
        num_x_hops[number][prb_id] = 0
        for hop in result["result"]:
            hop_number = hop["hop"]
            if not prb_id in num_consec_hops:
                num_consec_hops[number][prb_id] = hop_number
            elif num_consec_hops[number][prb_id] == hop_number-1: #hop not missed
                num_consec_hops[number][prb_id] = hop_number

            if hop["result"].has_key("x"):
                if hop_number==255:
                    reached_somewhere[number][prb_id] = False
                num_x_hops[number][prb_id] += 1
            
            elif hop["result"]["from"]==dst_addr:
                reached_dest[number][prb_id] = True
        num_hops[number][prb_id]=hop_number
        
        
#print(traceroutes)

#best_result ={}

final_result = []
icmp = []
tcp = []
udp = []
#for a particular destination:
for dst_ip in traceroutes:
 
    #for a particular probe to that destination:
    for prb_id in probe_ids[dst_ip]:
        #for all the measurements that go to that destination
        for number in traceroutes[dst_ip]:
            
            #find paris value:
            if number>2457509:
                paris=64
            elif number>2457306:
                paris=0
            else:
                paris=16
        
            #if there is a traceroute from this probe to this destination in this measurement
            if reached_somewhere[number].has_key(prb_id):
                if protocols[number]=="ICMP":
                    if len(icmp)>0:
                        icmp.append([paris, "{0:.2f}".format(float(latency[number][prb_id])), num_hops[number][prb_id], reached_dest[number][prb_id]])
                    else:
                        icmp = [[paris, "{0:.2f}".format(float(latency[number][prb_id])), num_hops[number][prb_id], reached_dest[number][prb_id]]]
                elif protocols[number]=="TCP":                        
                    if len(tcp)>0:
                        tcp.append([paris, "{0:.2f}".format(float(latency[number][prb_id])), num_hops[number][prb_id], reached_dest[number][prb_id]])
                    else:
                        tcp = [[paris, "{0:.2f}".format(float(latency[number][prb_id])), num_hops[number][prb_id], reached_dest[number][prb_id]]]
                elif protocols[number]=="UDP":                        
                    if len(udp)>0:
                        udp.append([paris, "{0:.2f}".format(float(latency[number][prb_id])), num_hops[number][prb_id], reached_dest[number][prb_id]])
                    else:
                        udp = [[paris, "{0:.2f}".format(float(latency[number][prb_id])), num_hops[number][prb_id], reached_dest[number][prb_id]]]                                                
#           else:
                #No measurement from this probe to this ip
        icmp.append(['-','-','-','-'])
        tcp.append(['-','-','-','-'])
        udp.append(['-','-','-','-'])

print("ICMP")
for row in icmp:
    for col in row:
        print(col, end="\t")
    print()
print("TCP")
for row in tcp:
    for col in row:
        print(col, end="\t")
    print()
print("UDP")
for row in udp:
    for col in row:
        print(col, end="\t")
    print()

#working with already aggregated/summarised data
from __future__ import print_function
import sys
import os
import json
from scipy.stats.mstats import normaltest
from scipy.stats import kruskal
from scipy.stats import f_oneway
import math


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
        reached_dest[number][prb_id] = False    
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
        
paris0_icmp = []
paris16_icmp = []
paris64_icmp = []
paris0_tcp = []
paris16_tcp = []
paris64_tcp = []
paris0_udp = []
paris16_udp = []
paris64_udp = []

icmp = []
tcp = []
udp = []

dest_icmp = 0.0
dest_udp = 0.0
dest_tcp = 0.0
count_icmp = 0.0
count_udp = 0.0
count_tcp = 0.0

#for a particular destination:
for dst_ip in traceroutes:
 
    #for a particular probe to that destination:
    for prb_id in probe_ids[dst_ip]:
        #for all the measurements that go to that destination
        for number in traceroutes[dst_ip]:
            #if there is a traceroute from this probe to this destination in this measurement
            if reached_somewhere[number].has_key(prb_id):
                if protocols[number]=="ICMP":
                    #set of latencies for icmp traceroutes
                    if len(icmp)>0:
                        icmp.append(float("{0:.2f}".format(float(latency[number][prb_id]))))
                    else:
                        icmp = [float("{0:.2f}".format(float(latency[number][prb_id])))]
                    if reached_somewhere[number][prb_id]:
                        count_icmp+=1
                    if reached_dest[number][prb_id]:
                        dest_icmp+=1
                    #find paris value:
                    if number>2457509:
                        #set of latencies for icmp traceroutes and paris=64                    
                        if len(paris64_icmp)>0:
                            paris64_icmp.append(float("{0:.2f}".format(float(latency[number][prb_id]))))
                        else:
                            paris64_icmp = [float("{0:.2f}".format(float(latency[number][prb_id])))]
                    elif number>2457306:
                        #set of latencies for icmp traceroutes and paris=0                    
                        if len(paris0_icmp)>0:
                            paris0_icmp.append(float("{0:.2f}".format(float(latency[number][prb_id]))))
                        else:
                            paris0_icmp = [float("{0:.2f}".format(float(latency[number][prb_id])))]
                    else:
                        #set of latencies for icmp traceroutes and paris=16                    
                        if len(paris16_icmp)>0:
                            paris16_icmp.append(float("{0:.2f}".format(float(latency[number][prb_id]))))
                        else:
                            paris16_icmp = [float("{0:.2f}".format(float(latency[number][prb_id])))]
                elif protocols[number]=="TCP":
                    #set of latencies for tcp traceroutes
                    if len(tcp)>0:
                        tcp.append(float("{0:.2f}".format(float(latency[number][prb_id]))))
                    else:
                        tcp = [float("{0:.2f}".format(float(latency[number][prb_id])))]
                    if reached_somewhere[number][prb_id]:
                        count_tcp+=1
                    if reached_dest[number][prb_id]:
                        dest_tcp+=1
                    #find paris value:
                    if number>2457509:
                        #set of latencies for tcp traceroutes and paris=64
                        if len(paris64_tcp)>0:
                            paris64_tcp.append(float("{0:.2f}".format(float(latency[number][prb_id]))))
                        else:
                            paris64_tcp = [float("{0:.2f}".format(float(latency[number][prb_id])))]
                    elif number>2457306:
                        #set of latencies for tcp traceroutes and paris=0
                        if len(paris0_tcp)>0:
                            paris0_tcp.append(float("{0:.2f}".format(float(latency[number][prb_id]))))
                        else:
                            paris0_tcp = [float("{0:.2f}".format(float(latency[number][prb_id])))]
                    else:
                        #set of latencies for tcp traceroutes and paris=16
                        if len(paris16_tcp)>0:
                            paris16_tcp.append(float("{0:.2f}".format(float(latency[number][prb_id]))))
                        else:
                            paris16_tcp = [float("{0:.2f}".format(float(latency[number][prb_id])))]
                elif protocols[number]=="UDP":
                    #set of latencies for udp traceroutes
                    if len(udp)>0:
                        udp.append(float("{0:.2f}".format(float(latency[number][prb_id]))))
                    else:
                        udp = [float("{0:.2f}".format(float(latency[number][prb_id])))]
                    if reached_somewhere[number][prb_id]:
                        count_udp+=1
                    if reached_dest[number][prb_id]:
                        dest_udp+=1
                    #find paris value:
                    if number>2457509:
                        #set of latencies for udp traceroutes and paris=64
                        if len(paris64_udp)>0:
                            paris64_udp.append(float("{0:.2f}".format(float(latency[number][prb_id]))))
                        else:
                            paris64_udp = [float("{0:.2f}".format(float(latency[number][prb_id])))]
                    elif number>2457306:
                        #set of latencies for udp traceroutes and paris=0
                        if len(paris0_udp)>0:
                            paris0_udp.append(float("{0:.2f}".format(float(latency[number][prb_id]))))
                        else:
                            paris0_udp = [float("{0:.2f}".format(float(latency[number][prb_id])))]
                    else:
                        #set of latencies for udp traceroutes and paris=16
                        if len(paris16_udp)>0:
                            paris16_udp.append(float("{0:.2f}".format(float(latency[number][prb_id]))))
                        else:
                            paris16_udp = [float("{0:.2f}".format(float(latency[number][prb_id])))]

print ("ANOVA for ICMP: ")
print(f_oneway(paris0_icmp, paris16_icmp, paris64_icmp))
#print ("Kruskal: ")
#print(kruskal(paris0_icmp, paris16_icmp, paris64_icmp))
print ("ANOVA for TCP: ")
print(f_oneway(paris0_tcp, paris16_tcp, paris64_tcp))
#print ("Kruskal: ")
#print(kruskal(paris0_tcp, paris16_tcp, paris64_tcp))
print ("ANOVA for UDP: ")
print(f_oneway(paris0_udp, paris16_udp, paris64_udp))

print ("ANOVA for protocols: ")
print(f_oneway(icmp, tcp, udp))
#print ("Kruskal: ")
#print(kruskal(paris0_udp, paris16_udp, paris64_udp))

print("ICMP: "+str(int(dest_icmp))+"/"+str(int(count_icmp)))
print((dest_icmp/count_icmp)*100)
print("TCP: "+str(int(dest_tcp))+"/"+str(int(count_tcp)))
print((dest_tcp/count_tcp)*100)
print("UDP: "+str(int(dest_udp))+"/"+str(int(count_udp)))
print((dest_udp/count_udp)*100)

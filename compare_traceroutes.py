#working with already aggregated/summarised data
from __future__ import print_function
import sys
import os
import json

folder = sys.argv[1]

#put traceroutes to same destination together in a dictionary {ip_address: [filename_1, filename_2, filename_3]}
traceroutes = {}
probe_ids = {}
protocols = {}
reached_dest = {}
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
    if number<2439524:
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

        latency[number][prb_id] = str(result["latency"])
        reached_dest[number][prb_id] = False
        num_x_hops[number][prb_id] = 0
        for hop in result["result"]:
            hop_number = hop["hop"]
            if not prb_id in num_consec_hops:
                num_consec_hops[number][prb_id] = hop_number
            elif num_consec_hops[number][prb_id] == hop_number-1: #hop not missed
                num_consec_hops[number][prb_id] = hop_number

            if hop["result"].has_key("x"):
#                if hop_number==255:
                    #reached_dest[number][result["prb_id"]] = False
                num_x_hops[number][prb_id] += 1
                
            elif hop["result"]["from"]==dst_addr:
                reached_dest[number][prb_id] = True
        num_hops[number][prb_id]=hop_number
        
       

for dst_ip in traceroutes:
    an_ip_reached = False
    count=0
    measurement_info = []
    results = {}
    gen_filename = folder+"/joined_with_paris/"+"hops_to_"+dst_ip+".json"
    final_result = []
    for number in traceroutes[dst_ip]:
        json_file = open(folder+"/result_for_"+str(number)+"_NEW_coords.json",'r')
        results[number] = json.load(json_file)
        json_file.close()

    
    for prb_id in probe_ids[dst_ip]:
        best_result=0
        for number in traceroutes[dst_ip]:
            if reached_dest[number].has_key(prb_id):
                if reached_dest[number][prb_id]:
                    an_ip_reached = True
                    count+=1
                    if count==1:
                        measurement_info=[[str(prb_id),str(dst_ip),str(number)]]
                    else:
                        measurement_info.append([str(prb_id),str(dst_ip),str(number)])
                    if best_result<=0:
                        best_result = number
                    else:
                        #check if this one is better
                        if num_x_hops[number][prb_id] < num_x_hops[best_result][prb_id]:
                            best_result = number
                        elif latency[number][prb_id] < latency[best_result][prb_id]:
                            best_result = number
                        elif num_hops[number][prb_id] < num_hops[best_result][prb_id]:
                            best_result = number
                else:
                    #Dest not reached for protocol
                    if best_result<=0:
                        best_result = number
                    else:
                        if num_consec_hops[number][prb_id] > num_consec_hops[best_result][prb_id]:
                            best_result = number
                        elif latency[number][prb_id] < latency[best_result][prb_id]:
                            best_result = number
                        elif num_x_hops[number][prb_id] < num_x_hops[best_result][prb_id]:
                            best_result = number
                    
 #           else:
                #No measurement from this probe to this ip
        if best_result > 0:
            for result in results[best_result]:
                if result["prb_id"] == prb_id:
                    if len(final_result)<=0:
                        final_result = [result]
                    else:
                        final_result.append(result)
                    break
    if not an_ip_reached:
        print("no measurement from probe "+str(prb_id)+" to dest "+str(dst_ip))
    
    if len(measurement_info)<4:
        for row in measurement_info:
            for col in row:
                print(col, end=" ")
            print()
        print()

#    with open(gen_filename,'w') as gen_file:
 #       gen_file.write(json.dumps(final_result))


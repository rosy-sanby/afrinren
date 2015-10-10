import os
import sys
import json

def compare_pairs(pair1, pair2, buddy):
#    print(json.dumps(pair1))
    #print
    #print(json.dumps(pair2))
    #print
    dests = []
    rtts = []
    if not pair1:
        print"0.o"
        return
    for hop in pair1["result"]:
        if hop["result"].has_key("from"):
            dests.append([str(hop["result"]["from"])])
            rtts.append([hop["result"]["rtt"]])
        else:
            dests.append(["x"])
            rtts.append(["*"])
    for hop in pair2["result"]:
        index = hop["hop"]-1
#        print(index)
        if index<len(dests)-1:
            if hop["result"].has_key("from"):
                dests[index].append(str(hop["result"]["from"]))
                rtts[index].append(hop["result"]["rtt"])
            else:
                dests[index].append("x")
                rtts[index].append("*")
        else:
            index=len(dests)-1
            if hop["result"].has_key("from"):
                dests[index].append(str(hop["result"]["from"]))
                rtts[index].append(hop["result"]["rtt"])
            else:
                dests[index].append("x")
                rtts[index].append("*")
    if buddy:    
        for hop in buddy["result"]:
            index = hop["hop"]-1
 #           print(index)
            if index<len(dests)-1:
                if hop["result"].has_key("from"):
                    dests[index].append(str(hop["result"]["from"]))
                    rtts[index].append(hop["result"]["rtt"])
                else:
                    dests[index].append("x")
                    rtts[index].append("*")
            else:
                index=len(dests)-1
                if hop["result"].has_key("from"):
                    dests[index].append(str(hop["result"]["from"]))
                    rtts[index].append(hop["result"]["rtt"])
                else:
                    dests[index].append("x")
                    rtts[index].append("*")
        
    for dest in dests:
        print(dest)
    for rtt in rtts:
        print(rtt)
    print


folder = "results/measurement_info/"

count=0
for filename in os.listdir(folder):
    #open the measurement info to get the description
    with open(folder+filename, 'r') as measure_info_file:
        measure_info = json.load(measure_info_file)        
        description = measure_info["description"].split(' ')
        actual_dest = measure_info["resolved_ips"][0].strip()
    #get a measurement id to work with
    measure_id = filename[filename.rfind('_')+1:filename.rfind('.')]
    #description = [Traceroute, protocol, from, probe, to, dst_addr, (dst,prb)/(as, is)]
    protocol = description[1].strip()
    from_probe = description[3].strip()
    dst_addr = description[5].strip()
    #check if this measurement was successful
    if not protocol+"_to_"+actual_dest+"("+measure_id+").json" in os.listdir("results/json/"):
        continue
    if description[6]=="(as":
        ref = None
    else: #ref is [target dst,probe buddy]
        ref = [description[6].split(',')[0].strip()[1:], description[6].split(',')[1].strip()[:-1]]
    #find full traceroute to compare to
    pair1={}
    buddy={}
    for json_file in os.listdir("results/json/"):
        if json_file[:json_file.find('(')]==protocol+"_to_"+dst_addr and int(json_file[json_file.find('(')+1:json_file.find(')')])<2487080:
            print(json_file)
            with open("results/json/"+json_file, 'r') as full_trace:
                results = json.load(full_trace)
            for result in results:
                if result.has_key("prb_id") and int(result["prb_id"])==int(from_probe):
                    pair1=result
                    #break
                elif ref:
                    if result.has_key("prb_id") and int(result["prb_id"])==int(ref[1]):
                        buddy=result
                else:
                    continue
            break
        else:
            continue
    with open("results/json/"+protocol+"_to_"+actual_dest+"("+measure_id+").json", 'r') as overlap_trace:
        pair2 = json.load(overlap_trace)[0]

    print(str(from_probe)+" "+dst_addr+" actual:"+actual_dest)
    compare_pairs(pair1, pair2, buddy)
    #if count>2:
     #   break
    #else:
     #   count+=1

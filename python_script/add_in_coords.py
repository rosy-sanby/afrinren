import json
import sys
import os

#usage to make sure correct arguments supplied
#if len(sys.argv)!=2:
 #   print("specify python file, and folder with json file to edit and where to get coords\neg: python add_in_coords.py foldername")
  #  sys.exit(1)
folder = "results"
folder = folder+"/NEW"
for filename in os.listdir(folder):
    #print(filename_infolder)
    #continue
    skip = False
    k=filename[:filename.rfind("_")-1].rfind("_")
    for i in os.listdir("results/json"):
        if len(i.split('('))>1 and filename[k+1:filename.rfind("_")]+").json" == i.split('(')[1]:
            print("done: "+filename)
            skip = True
            break
    if skip:
        continue
    else:
        print("Adding in coords: "+filename)
#    print(filename[k+1:filename.rfind("_")])
    filename=folder+"/"+filename   #get filename to which to add coords
#    if filename_infolder=="NEW"
    newfilename = folder+"/../json"+filename[len(folder):-5]+"_coords"+filename[-5:]    #generate new filename
    hop_ips = open(folder+"/../hop_coords"+filename[len(folder):-8]+"hop_coords",'r')   #open a file from which to read all the hop ip addresses and coords
    hop_asns = open(folder+"/../hop_asns"+filename[len(folder):-8]+"hop_asns",'r')
    #else:
       # continue
    probe_file = open("data/my_probes.txt", 'r')
    probe_info = probe_file.readlines()    
    probe_file.close()
    with open(filename,'r') as json_data:
        results = json.load(json_data)
        if len(results)<=0:
            continue
        dst_asn=0
        not_done = []
        for result in results:
            rtt=0
            if result.has_key("lts"):
                del result["lts"]
            if result.has_key("endtime"):
                del result["endtime"]
            if result.has_key("fw"):
                del result["fw"]
            if result.has_key("af"):
                del result["af"]                                    
            for hop in result["result"]:
                if hop["result"].has_key("from"):
                    hop_details = hop_ips.readline().split(', ')
                    hop_details_asn = hop_asns.readline().split(', ')
                    if hop["result"]["from"]==hop_details[0].strip():
                        if len(hop_details)>3:
                            hop["result"]["public"] = True
                            hop["result"]["country"] = hop_details[2].strip()[6:].strip()
                            if hop_details[5].strip()=="City of":
                                hop["result"]["coordinates"] = [float(hop_details[8].strip()), float(hop_details[9].strip())]
                            else:
                                hop["result"]["coordinates"] = [float(hop_details[7].strip()), float(hop_details[8].strip())]
                        else:
                            hop["result"]["public"] = False
                    if hop["result"]["from"]==hop_details_asn[0].strip():
                        if not hop_details_asn[1].split(': ')[1].strip() == "IP Address not found":
                            hop["result"]["asn"] = int(hop_details_asn[1].split(': ')[1].strip()[2:hop_details_asn[1].split(': ')[1].strip().find(" ")])
                    if hop["result"]["from"]==result["dst_addr"] and hop["result"].has_key("asn"):
                        dst_asn = hop["result"]["asn"]
                if hop["result"].has_key("rtt"):
                    rtt = hop["result"]["rtt"]
                
            
            result["latency"] = rtt
            if dst_asn>0:
                result["dst_asn"] = dst_asn
            else:
                if len(not_done)>0:
                    not_done.append(result)
                else:
                    not_done = [result]
            for line in probe_info:
                if int(line.split(" ")[0])==result["prb_id"]:
                    result["src_asn"] = int(line.split(" ")[1])
                    break
        for result in not_done:
            if dst_asn>0:
                result["dst_asn"] = dst_asn
                           
    hop_ips.close()
    hop_asns.close()  
    with open(newfilename,'w') as json_data:
        json_data.write(json.dumps(results))

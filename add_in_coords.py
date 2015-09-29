import json
import sys
import os

#usage to make sure correct arguments supplied
if len(sys.argv)!=2:
    print("specify python file, and folder with json file to edit and where to get coords\neg: python add_in_coords.py foldername")
    sys.exit(1)

folder = sys.argv[1]
folder = folder+"/NEW"
for filename in os.listdir(folder):
    #print(filename_infolder)
    #continue
    k=filename[:filename.rfind("_")-1].rfind("_")
    if int(filename[k+1:filename.rfind("_")])<2457510:
        continue
#    print(filename[k+1:filename.rfind("_")])
    filename=folder+"/"+filename   #get filename to which to add coords
#    if filename_infolder=="NEW"
    newfilename = folder+"/../json"+filename[len(folder):-5]+"_coords"+filename[-5:]    #generate new filename
    hop_ips = open(folder+"/../hop_coords"+filename[len(folder):-8]+"hop_coords",'r')   #open a file from which to read all the hop ip addresses and coords
    #else:
       # continue
        
    with open(filename,'r') as json_data:
        results = json.load(json_data)
        
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
                    if hop["result"]["from"]==hop_details[0].strip():
                        if len(hop_details)>3:
                            hop["result"]["public"] = True
                            hop["result"]["country"] = hop_details[2].strip()[6:].strip()
                            if hop_details[5].strip()=="City of":
                                hop["result"]["coordinates"] = [hop_details[8].strip(), hop_details[9].strip()]
                            else:
                                hop["result"]["coordinates"] = [hop_details[7].strip(), hop_details[8].strip()]
                        else:
                            hop["result"]["public"] = False
                if hop["result"].has_key("rtt"):
                    rtt = hop["result"]["rtt"]
            result["latency"] = rtt
                           
    hop_ips.close()        
    with open(newfilename,'w') as json_data:
        json_data.write(json.dumps(results))

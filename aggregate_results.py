import os
import json
import sys
from subprocess import call

#usage to make sure correct arguments supplied
if len(sys.argv)!=2:
    print("specify python file and folder with json files to edit\neg: python aggregate_results.py results")
    sys.exit(1)

folder = sys.argv[1]
pings = open(folder+"/pingsNeeded_TCP",'w')
#count=0
for filename in os.listdir(folder):
    #print(filename)
    k = filename.rfind("_")
    if filename[-5:]!=".json" or filename[-8:]=="NEW.json" or int(filename[k+1:-5])<2442490:
        continue

    filename = folder+"/"+filename
    newfilename = folder+"/NEW"+filename[len(folder):-5]+"_NEW"+filename[-5:]    #generate new filename
    hop_ip_filename = folder+"/hop_ips"+filename[len(folder):-5]+"_hop_ips.txt"
    hop_coords = folder+"/hop_coords"+filename[len(folder):-5]+"_hop_coords"
    hop_ips = open(hop_ip_filename,'w')   #open a file to write all the hop ip addresses to
    

    with open(filename,'r') as json_data:
        results = json.load(json_data)
        total_rtt = 0.0
        num_rtt = 0.0
        num_x = 0
        for result in results:
            dst_addr = result["dst_addr"]
            src_addr = result["src_addr"]
            prb_id = result["prb_id"]
            for hop in result["result"]:
                for packet in hop["result"]:
                    if packet.has_key("from"):
                        fromIP=packet["from"]
                    if packet.has_key("rtt"):
                        total_rtt += packet["rtt"]
                        num_rtt += 1                  
                    elif packet.has_key("x") :
                        num_x += 1
                        
                if (num_rtt>0):
                    hop["result"]={"from":fromIP,"rtt":total_rtt/num_rtt}
                    hop_ips.write(fromIP+"\n") 
                elif (num_x>0):
                    hop["result"]={"x":"*"}
                total_rtt = 0.0
                num_rtt = 0.0
                if hop.has_key("hop"):
                    hop_no=hop["hop"]
            if hop_no>250 and num_x>0:
                #print("ping needed, I think from: "+str(prb_id)+" ip: "+src_addr+" to: "+dst_addr)
                pings.write(dst_addr+" "+str(prb_id)+'\n')
            #else:
             #   count+=1
              #  print(count)
            num_x = 0
            hop_no = 0
            
    hop_ips.close()
    
    #print(hop_ip_filename)
    #print(hop_coords)
    myfile = open(hop_coords,'w')
    call(["sh","geoip.sh",hop_ip_filename], stdout=myfile)
    myfile.close()
            
    with open(newfilename,'w') as json_data:
        json_data.write(json.dumps(results))
pings.close()       
#    break

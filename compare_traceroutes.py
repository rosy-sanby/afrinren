import sys
import os
import json

folder = sys.argv[1]

#put traceroutes to same destination together in a dictionary {ip_address: [filename_1, filename_2, filename_3]}
traceroutes = {}
for filename in os.listdir(folder):
    if filename[-5:]!=".json":
        continue
    k=filename.rfind("_")
    number = int(filename[k+1:filename.rfind(".")])
    #print(number)
    if number<2439524:
        continue
    
    json_data = open(folder+filename,'r')
    json_info = json.load(json_data)
    json_data.close()
    dst_addr = json_info[0]["dst_addr"]
    if not dst_addr in traceroutes:
        traceroutes[dst_addr] = [number]
    else:
        traceroutes[dst_addr].append(folder+filename)
        
#print(traceroutes)

for key in traceroutes:
    results = []
    for filename in traceroutes[key]:
        results.append(json.load(open(filename,'r')))
        filename.close()
        
    for one_result in results:
        total_rtt = 0.0
        num_rtt = 0.0
        num_x = 0
        for result in one_result:
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
                    #hop_ips.write(fromIP+"\n") 
                elif (num_x>0):
                    hop["result"]={"x":"*"}
                total_rtt = 0.0
                num_rtt = 0.0
                if hop.has_key("hop"):
                    hop_no=hop["hop"]
            if hop_no>250 and num_x>0:
                #print("ping needed, I think from: "+str(prb_id)+" ip: "+src_addr+" to: "+dst_addr)
            num_x = 0
            hop_no = 0

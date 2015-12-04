#working with already aggregated/summarised data
from __future__ import print_function
import sys
import os
import json

#Node for creating tree
class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parents = []
        self.weight = 1
        self.destinations = []
        self.hop_no = 1

    def add_child(self, obj):
        self.children.append(obj)
    
    def add_parent(self, obj):
        self.parents.append(obj)
    
    def add_weight(self):
        self.weight += 1

    def add_destination(self, obj):
        if not obj in self.destinations:        
            self.destinations.append(obj)

    def set_hop_no(self, num):
        self.hop_no = num
        
    def print_out(self, count):
        if len(self.children)<=0:
            print('-'*count+str(self.hop_no)+": "+self.data+" "+str(self.weight))
        else:
            print('-'*count+str(self.hop_no)+": "+self.data+" "+str(self.weight))
            count+=1
            for child in self.children:
                child.print_out(count)

folder = sys.argv[1] # in general results/json
my_protocol = sys.argv[2] #UDP or TCP or ICMP
trees = {}
line_number=1
all_dsts = []

with open("data/address_african",'r') as addresses:
    for line in addresses.readlines():
        all_dsts.append(line.strip())

##########make trees########################################
for filename in os.listdir(folder):
    if filename[-5:]!=".json":
        continue
    protocol = filename[:filename.find("_")]
    k=filename.find("(")
    number = int(filename[k+1:filename.find(")")])
    if (number>2487079 and number<2802359) or (number>2810085 and number<2901361):#not full:
        continue
    if not protocol==my_protocol: #only selects certain protocol measurements
        continue
    
    with open(folder+"/"+filename,'r') as json_data:
        results = json.load(json_data)
        first_result = True
        for result in results:
            prb_id = result["prb_id"]
            dst_addr = result["dst_addr"]
            if not dst_addr in all_dsts:
                continue
            if not prb_id in trees: #if this probe hasn't been seen yet
                trees[prb_id] = ""
            node = trees[prb_id] #set current node to root of tree of the probe
            for hop in result["result"]:
                if hop["result"].has_key("from"):
                    ip_addr = hop["result"]["from"]
                else:
                    ip_addr = "x"
                #construct trees to find overlaps at beginning
                if isinstance(node, Node): #if this is already a Node,
                    if ip_addr=="x":
                        new_child = Node(ip_addr)
                        node.add_child(new_child)
                        new_child.set_hop_no(node.hop_no+1)
                        node.add_destination(dst_addr)
                        new_child.add_parent(node)
                        new_child.add_destination(dst_addr)
                        node = new_child
                    elif node.data == ip_addr: #check if the ip_addresses are the same
                        node.add_weight()
                        node.add_destination(dst_addr)
                    else:   #check if a child has same ip address
                        child_found = False
                        for child in node.children:
                            if child.data == ip_addr:
                                child_found = True
                                child.add_weight()
                                child.add_destination(dst_addr)
                                node = child
                                break
                        if not child_found:
                            new_child = Node(ip_addr)
                            node.add_child(new_child)
                            new_child.set_hop_no(node.hop_no+1)
                            node.add_destination(dst_addr)
                            new_child.add_parent(node)
                            new_child.add_destination(dst_addr)
                            node = new_child
                else:
                    node = Node(ip_addr)
                    node.add_destination(dst_addr)
                    trees[prb_id] = node


##############trees made - find overlaps now############################
hop_ips = {} #dictionary by probe id to show paths
for filename in os.listdir(folder):
    if filename[-5:]!=".json":
        continue
    protocol = filename[:filename.find("_")]
    k=filename.find("(")
    number = int(filename[k+1:filename.find(")")])
    if (number>2487079 and number<2802359) or (number>2810085 and number<2901361): #not full
        continue
    if not protocol==my_protocol:
        continue
    
    
    with open(folder+"/"+filename,'r') as json_data:
        results = json.load(json_data)
        for result in results:
            prb_id = result["prb_id"]
            dst_addr = result["dst_addr"]
            if not dst_addr in all_dsts:
                continue
            if hop_ips.has_key(prb_id):
                if hop_ips[prb_id].has_key(dst_addr):
                    continue
                hop_ips[prb_id][dst_addr] = [] #to get the path for this particular probe-dest pair
            else:
                hop_ips[prb_id]={}
            hop_ips[prb_id][dst_addr] = [] #to get the path for this particular probe-dest pair
            for hop in result["result"]:
                if hop["result"].has_key("from"):
                    ip_addr = hop["result"]["from"]
                else:
                    ip_addr = "x"
                #find overlaps at end
                hop_ips[prb_id][dst_addr].append(ip_addr)
        
end_ips = {} #dictonary by destination address to see which probes follow same path near destination
for prb_id in hop_ips:
    for dst_addr in hop_ips[prb_id]:
        for hop_ip in hop_ips[prb_id][dst_addr]:
            if end_ips.has_key(dst_addr):
                if end_ips[dst_addr].has_key(hop_ip):
                    if prb_id in end_ips[dst_addr][hop_ip]:
                        continue
                    else:
                        end_ips[dst_addr][hop_ip].append(prb_id)
                else:
                    end_ips[dst_addr][hop_ip] = [prb_id]
            else:
                end_ips[dst_addr]={}
                end_ips[dst_addr][hop_ip] = [prb_id]
        
        
               
#check if an end path is copied in any other hop_ips path(s)
partial = {} #dictionary [probe][dest]=[first_hop, max_hop]

all_probes = [14900, 13114, 13218, 4061, 4096, 14867, 3461, 4518, 18114, 18169, 13721, 14712]
       
###########################overlaps at beginning#########################################3                    
for probe in all_probes:
       
    curr_node = trees[probe]
    too_few=False
    for dst_addr in hop_ips[probe]:
        while dst_addr in curr_node.destinations and curr_node.weight>2 and not too_few:
            child_found=False
            for child in curr_node.children:
                if dst_addr in child.destinations:
                    if child.weight<5:
                        too_few=True
                        break
                    curr_node=child #NOTE does this overwrite the curr_node?
                    child_found=True

                    break
            if not child_found:
                break
       
        first_hop = curr_node.hop_no

        if not partial.has_key(probe):
            partial[probe]={}
            partial[probe][dst_addr] = [first_hop,125]
        elif not partial[probe].has_key(dst_addr):
            partial[probe][dst_addr] = [first_hop,125]
        elif partial[probe][dst_addr][0]<first_hop:
            partial[probe][dst_addr] = [first_hop,125]
 

##################overlaps at end#########################################3
for prb_id in all_probes:
   
    for dst_addr in hop_ips[prb_id]:
      
        same_path_probes = []
        new_end = dst_addr
        for hop_ip in hop_ips[prb_id][dst_addr]:
            if len(end_ips[dst_addr][hop_ip])<=1: #if only one probe went through this hop to get to this dest
                continue
            else: #something else goes along this path
                if len(same_path_probes)<=0:
                    if not hop_ip==dst_addr and not hop_ip=="x":
                        for probe in end_ips[dst_addr][hop_ip]:
                            same_path_probes.append(probe)
                        new_end = hop_ip
                else:
                    for el in same_path_probes:
                        if not el in end_ips[dst_addr][hop_ip]: #check if they all continue on the same path
                            same_path_probes = []
                            new_end = dst_addr
                            break
            for my_probe in same_path_probes:
             
                max_hop = hop_ips[my_probe][dst_addr].index(new_end)
                while partial[my_probe][dst_addr][0]>=max_hop:
                    max_hop+=1
                partial[my_probe][dst_addr][1] = max_hop
                    
                            

for probe in partial:
    for dest in partial[probe]:
        print (my_protocol+": "+str(probe)+" "+dest+" ["+str(partial[probe][dest][0])+","+str(partial[probe][dest][1])+"]")
 

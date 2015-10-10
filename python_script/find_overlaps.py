#working with already aggregated/summarised data
from __future__ import print_function
import sys
import os
import json

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
            #if self.weight>1:
            print('-'*count+str(self.hop_no)+": "+self.data+" "+str(self.weight))
        else:
            #if self.weight>1:
            print('-'*count+str(self.hop_no)+": "+self.data+" "+str(self.weight))
            count+=1
            for child in self.children:
                child.print_out(count)

folder = sys.argv[1] # in general results/json
trees = {}

##########make trees########################################
for filename in os.listdir(folder):
    if filename[-5:]!=".json":
        continue
    protocol = filename[:filename.find("_")]
    k=filename.find("(")
    number = int(filename[k+1:filename.find(")")])
    #print(number)
    if number<2439524 or (number<2457306 and number>2456864):
        continue
    if not protocol=="UDP":
        continue
    
    with open(folder+"/"+filename,'r') as json_data:
        results = json.load(json_data)
        first_hops = {}
        first_result = True
        for result in results:
            prb_id = result["prb_id"]
            dst_addr = result["dst_addr"]
            if not prb_id in trees: #if this probe hasn't been seen yet
                trees[prb_id] = ""
                #print("New root: "+str(prb_id))
            #else:
                #print("Root seen already: "+ str(prb_id))
            node = trees[prb_id] #set current node to root of tree of the probe
            first_hops[prb_id] = []              
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
                        if node.weight>5:
                            first_hops[prb_id] = [dst_addr, hop["hop"], node.weight]
                        #print("Node seen again: "+ip_addr)
                    else:   #check if a child has same ip address
                        child_found = False
                        for child in node.children:
                            if child.data == ip_addr:
                                child_found = True
                                child.add_weight()
                                child.add_destination(dst_addr)
                                if child.weight>5:
                                    first_hops[prb_id] = [dst_addr, hop["hop"], node.weight]
                                node = child
                                break
                        if not child_found:
                            new_child = Node(ip_addr)
                            node.add_child(new_child)
                            new_child.set_hop_no(node.hop_no+1)
                            node.add_destination(dst_addr)
                            new_child.add_parent(node)
                            new_child.add_destination(dst_addr)
                            #print("New child added: "+ip_addr)
                            node = new_child
                else:
                    node = Node(ip_addr)
                    node.add_destination(dst_addr)
                    trees[prb_id] = node


##############trees made - find overlaps now############################
for filename in os.listdir(folder):
    if filename[-5:]!=".json":
        continue
    protocol = filename[:filename.find("_")]
    k=filename.find("(")
    number = int(filename[k+1:filename.find(")")])
    #print(number)
    if number<2439524 or (number<2457306 and number>2456864):
        continue
    if not protocol=="UDP":
        continue
    
    
    with open(folder+"/"+filename,'r') as json_data:        
        hop_ips = {}
        results = json.load(json_data)
        for result in results:
            prb_id = result["prb_id"]
            dst_addr = result["dst_addr"]
            hop_ips[prb_id] = []
            for hop in result["result"]:
                if hop["result"].has_key("from"):
                    ip_addr = hop["result"]["from"]
                else:
                    ip_addr = "x"
                #find overlaps at end
                hop_ips[prb_id].append(ip_addr)
        
        end_ips = {}
        for prb_id in hop_ips:
            for hop_ip in hop_ips[prb_id]:
                if end_ips.has_key(hop_ip):
                    if prb_id in end_ips[hop_ip]:
                        continue
                    else:
                        end_ips[hop_ip].append(prb_id)
                else:
                    end_ips[hop_ip] = [prb_id]
        
        #check if an end path is copied in any other hop_ips path(s)
        prbs_to_miss = []
        for prb_id in hop_ips:
            
            if prb_id in prbs_to_miss:
                #print()
                continue
            #print(prb_id)
            same_path_probes = []
            new_end = dst_addr
            for hop_ip in hop_ips[prb_id]:
                if len(end_ips[hop_ip])<=1:
                    continue
                else: #something else goes along this path
                    if len(same_path_probes)<=0:
                        if not hop_ip==dst_addr and not hop_ip=="x":
                            for probe in end_ips[hop_ip]:
                                same_path_probes.append(probe)
                            new_end = hop_ip
                    else:
                        for el in same_path_probes:
                            if not el in end_ips[hop_ip]: #check if they all continue on the same path
                                same_path_probes = []
                                new_end = dst_addr
                                break
            
            if prb_id in same_path_probes:
                same_path_probes.remove(prb_id)
            #    curr_node = trees[prb_id]
             #   too_few=False

#                while dst_addr in curr_node.destinations and curr_node.weight>2 and not too_few:
 #                   child_found=False
  #                  for child in curr_node.children:
   #                     if dst_addr in child.destinations:
    #                        if child.weight<5:
     #                           too_few=True
      #                          break
       #                     curr_node=child #does this overwrite the curr_node?
        #                    child_found=True
         #                   break
          #          if not child_found:
           #             break

                #print(str(prb_id)+" "+dst_addr+" "+str(curr_node.hop_no)+" "+ curr_node.destinations[0]+" "+dst_addr+" "+str(prb_id))
                
            for probe in prbs_to_miss:
                if probe in same_path_probes:
                    same_path_probes.remove(probe)
            for probe in same_path_probes:
                prbs_to_miss.append(probe)

 #               print(str(probe)+" to "+new_end+" (same as "+str(prb_id)+")")
                
                #need to wait for whole tree to be built for this...
       #         curr_node_dests = []
      #          for dest in trees[probe].destinations:
     #               curr_node_dests.append(dest)
    #            curr_node_weight = trees[probe].weight
   #             curr_node_children = []
  #              for child in trees[probe].children:
 #                   curr_node_children.append(child)
#                curr_node_hop = trees[probe].hop_no
                curr_node = trees[probe]
                too_few=False

                while dst_addr in curr_node.destinations and curr_node.weight>2 and not too_few:
                    child_found=False
                    for child in curr_node.children:
                        if dst_addr in child.destinations:
                            if child.weight<5:
                                too_few=True
                                break
                            curr_node=child #does this overwrite the curr_node?
                            child_found=True
#                            curr_node_dests = []
 #                           for dest in child.destinations:
  #                              curr_node_dests.append(dest)
   #                         curr_node_weight = child.weight
    #                        curr_node_children = []
     #                       for child in child.children:
      #                          curr_node_children.append(child)
       #                     curr_node_hop = child.hop_no
                            break
                    if not child_found:
                        break

                if curr_node.hop_no>1 and len(curr_node.destinations)>1:
                    curr_node.weight=curr_node.weight-1
                    curr_node.destinations.remove(dst_addr)
#                print("probe "+str(probe)+" to "+dst_addr+": "+str(curr_node.hop_no)+" "+str(curr_node.weight))
                    print(str(probe)+" "+dst_addr+" "+str(curr_node.hop_no)+" "+ curr_node.destinations[0]+" "+new_end+" "+str(prb_id))
                else:
                    print(str(probe)+" "+dst_addr+" "+str(curr_node.hop_no)+" "+ dst_addr+" "+new_end+" "+str(prb_id))
            

#print(trees[probe].destinations)
 #               print(trees[probe].weight)


        #for key in end_ips:        
        #    if len(end_ips[key])>1: 
    
        #        print(key,end=": ")
        #        print(end_ips[key])
#        for prb_id in first_hops:
 #           print(prb_id, end= ', ')
  #          print(first_hops[prb_id])
   #         print()
        
           # print(str(prb_id), end=" - ")
          #  for hop_ip in hop_ips[prb_id]:
       #         print(hop_ip, end=", ")
         #   print('\n')
        #break
#for probe in trees:
#    trees[probe].print_out(1)

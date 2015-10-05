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

    def add_child(self, obj):
        self.children.append(obj)
    
    def add_parent(self, obj):
        self.parents.append(obj)
    
    def add_weight(self):
        self.weight += 1
        
    def print_out(self, count):
        if len(self.children)<=0:
            print('-'*count+self.data+" "+str(self.weight))
        else:
            print('-'*count+self.data+" "+str(self.weight))
            count+=1
            for child in self.children:
                child.print_out(count)

folder = sys.argv[1] # in general results/json
trees = {}
for filename in os.listdir(folder):
    if filename[-5:]!=".json":
        continue
    k=filename[:filename[:filename.rfind("_")-1].rfind("_")].rfind("_")
    number = int(filename[k+1:filename[:filename.rfind("_")-1].rfind("_")])
    #print(number)
    if number<2439524 or (number<2457306 and number>2456864):
        continue
    
    
    with open(folder+"/"+filename,'r') as json_data:
        results = json.load(json_data)
        for result in results:
            prb_id = result["prb_id"]
            if not prb_id in trees: #if this probe hasn't been seen yet
                trees[prb_id] = ""
                #print("New root: "+str(prb_id))
            #else:
                #print("Root seen already: "+ str(prb_id))
            node = trees[prb_id] #set current node to root of tree of the probe
                
            for hop in result["result"]:
                if hop["result"].has_key("from"):
                    ip_addr = hop["result"]["from"]
                else:
                    ip_addr = "x"
                if isinstance(node, Node): #if this is already a Node,
                    if ip_addr=="x":
                        new_child = Node(ip_addr)
                        node.add_child(new_child)
                        new_child.add_parent(node)
                        node = new_child
                    elif node.data == ip_addr: #check if the ip_addresses are the same
                        node.add_weight()
                        #print("Node seen again: "+ip_addr)
                    else:   #check if a child has same ip address
                        child_found = False
                        for child in node.children:
                            if child.data == ip_addr:
                                child_found = True
                                child.add_weight()
                                node = child
                                break
                        if not child_found:
                            new_child = Node(ip_addr)
                            node.add_child(new_child)
                            new_child.add_parent(node)
                            #print("New child added: "+ip_addr)
                            node = new_child
                else:
                    node = Node(ip_addr)
                    trees[prb_id] = node
for probe in trees:
    trees[probe].print_out(0)
    break                 

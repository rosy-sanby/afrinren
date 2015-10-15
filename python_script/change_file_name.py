import sys
import os
import json

folder = "results/json"
for filename in os.listdir(folder):
    if not filename[:filename.find('_')]=="result":
        continue
    with open(folder+"/"+filename, 'r') as measurement:
        results = json.load(measurement)
        dst_addr = results[0]["dst_addr"]
        measurement_id = results[0]["msm_id"]
        protocol = results[0]["proto"]
    new_filename = protocol+"_to_"+dst_addr+"("+str(measurement_id)+").json"
    print(folder+"/"+filename)
    print(folder+"/"+new_filename)
    print()
    os.rename(folder+"/"+filename, folder+"/"+new_filename)

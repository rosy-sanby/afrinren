import sys
import os
import json

folder = sys.argv[1]

for protocol in os.listdir(folder):
    for filename in os.listdir(folder+"/"+protocol):
        with open(folder+"/"+protocol+"/"+filename, 'r') as measurement:
            results = json.load(measurement)
            dst_addr = results[0]["dst_addr"]
            measurement_id = results[0]["msm_id"]
        new_filename = protocol+"_to_"+dst_addr+"("+str(measurement_id)+").json"
        print(folder+"/"+protocol+"/"+filename)
        print(folder+"/"+protocol+"/"+new_filename)
        os.rename(folder+"/"+protocol+"/"+filename, folder+"/"+protocol+"/"+new_filename)

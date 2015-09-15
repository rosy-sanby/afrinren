import json
import sys

#usage to make sure correct arguments supplied
if len(sys.argv)!=2:
    print("specify python file and json file to edit\neg: python convert_to_geojson.py json_file.json")
    sys.exit(1)

filename = sys.argv[1]  #get filename to which to add coords
newfilename = filename[:-11]+"_geojson"+filename[-5:]    #generate new filename

with open(filename,'r') as json_data:
    results = json.load(json_data)
    #geojson = {}
    #geojson["type"] = "FeatureCollection"
    #geojson["features"] = []
    coords = {}
    for result in results:
        for hop in result["result"]:
            if hop["result"].has_key("from") and hop["result"].has_key("coordinates"):
                coords[hop["result"]["from"]] = hop["result"]["coordinates"]
            
            
    geojson = json.dumps({ "type": "FeatureCollection",
                            "features": [ 
                                            {"type": "Feature",
                                             "geometry": { "type": "Point",
                                                           "coordinates": [coords[] ]},
                                             "properties": { key: value 
                                                             for key, value in result.items()
                                                             if key not in ('result') }
                                             } 
                                         for result in results
                                        ]
                           })
                       
with open(newfilename,'w') as json_data:
    json_data.write(geojson)
    
#"type": "FeatureCollection",
 #  "features": [
 # {
 #   "type": "Feature",
 #   "geometry": {
  #     "type": "Point",
  #     "coordinates":  [ 32.570989,0.329179 ]
 #   },
 #   "properties": {
#    "measurement_id":15357,
#    "measurement_dat":327687,
#    "target_ip":"RENU",
#	"probe": ,
 #   "protocol":"ICMP",
#	"latency": 167,
#	"rtt":,
#	}

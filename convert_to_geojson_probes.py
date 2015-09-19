import json
import sys

#usage to make sure correct arguments supplied
#if len(sys.argv)!=2:
 #   print("specify python file and text file to get info\neg: python convert_to_geojson.py json_file.json")
  #  sys.exit(1)

filename = sys.argv[1]  #get filename to which to add coords
newfilename = "probes.json"    #generate new filename
probes = open(filename, 'r')
lines = probes.readlines()
probes.close()

as_file = open(sys.argv[2],'r')
as_info = as_file.readlines()
as_file.close()
#for line in as_info:
 #   line = line.split("; ")     #[type, asn, name]

geojson = {}
geojson["type"] = "FeatureCollection"
geojson["features"] = []
coords = {}
count = 0
as_name=""
as_type=""

for line in lines:
    probe_info = line.split(" ")    #[probe_id, asn, lat, long]
    for asn in as_info:
        #print(probe_info[1]+" and "+asn.split("; ")[1])
        if probe_info[1]==asn.split("; ")[1]:
            as_name=asn.split("; ")[2].strip()
            as_type=asn.split("; ")[0].strip()
            break
#    print(count)
    geojson["features"].append({"type":"Feature", "geometry":{"type": "Point", "coordinates": [probe_info[2],probe_info[3].strip()]}, "properties":{"probe_id":probe_info[0], "asn":probe_info[1], "name": as_name, "type": as_type}})
    
    count+=1
    as_name=""
    as_type=""
            
    #geojson = json.dumps({ "type": "FeatureCollection",
     #                       "features": [ 
      #                                      {"type": "Feature",
       #                                      "geometry": { "type": "Point",
        #                                                   "coordinates": [coords[] ]},
         #                                    "properties": { key: value 
          #                                                   for key, value in result.items()
           #                                                  if key not in ('result') }
            #                                 } 
             #                            for result in results
              #                          ]
               #            })
                       
with open(newfilename,'w') as json_data:
    json_data.write(json.dumps(geojson))

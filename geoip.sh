#!/usr/bin/bash
filename="$1"
while read -r ADDR
do
   RESULT=`geoiplookup "${ADDR}" -f /home/rosy/Documents/Honours/afrinren/GeoLiteCity.dat`
   echo "${ADDR}", "${RESULT}"
done < "$filename"

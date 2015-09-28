#!/usr/bin/bash
filename="$1"
while read -r ADDR
do
   RESULT=`geoiplookup "${ADDR}" -f /home/s/snbros001/Documents/Me/AFRINREN/snbros001/GeoLiteCity.dat`
   echo "${ADDR}", "${RESULT}"
done < "$filename"

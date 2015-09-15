#!/bin/sh

# general instructions for geoip: http://dev.maxmind.com/geoip/legacy/install/city/
# install geoiplookup tool and default db; on ubuntu its 'apt-get install geoip-bin geoip-database'
# download MaxMinx GeoLite databases from here: http://dev.maxmind.com/geoip/legacy/geolite/ ; you probably want the the GeoLite ASN and GeoLite City
# extract the dbs to a location of your choice, and specify -f in script below.
# run the script with ip-list file: ./geoip.sh ip-list-file ("address_all") 
# sh geoip.sh address_all

while read ADDR
do
RESULT=`geoiplookup "${ADDR}" -f /home/s/snbros001/Documents/Me/AFRINREN/snbros001/GeoLiteCity.dat` # specify path the db file here
echo "${ADDR}", "${RESULT}"
done < $1


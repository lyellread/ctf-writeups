#!/bin/bash

# get a list of image IDs in all_ids.txt
for i in {0..100}; do
    curl "http://challs.houseplant.riceteacatpanda.wtf:30002/api?page=$i&limit=10000" | jq -r '.data | .[].id' >> all_ids.txt
done

# pull each image by ID from all_ids.txt into all_cats/
mkdir all_cats
for line in $(cat all_ids.txt); do
    wget "http://challs.houseplant.riceteacatpanda.wtf:30002/images/$line.jpg" -O "all_cats/$line.jpg"
done

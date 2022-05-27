#! /bin/bash
#generates files, like 2022-May-27--0000.zip
DATE=2021-01-01
cd /var/atlassian/application-data/jira/export/

for i in {0..365}; do
	DATE1=$(date +%Y-%m-%d -d "$DATE + $i day")
	DATE2=$(date +%Y_%h_%d -d "$DATE + $i day")
	
	dd if=/dev/urandom of=$DATE2--0000.zip bs=1 count=$(( RANDOM + 1024 ))
	dd if=/dev/urandom of=$DATE2--1200.zip bs=1 count=$(( RANDOM + 1024 ))

	touch -m --date="$DATE1 00:05" $DATE2--0000.zip
	touch -m --date="$DATE1 12:05" $DATE2--1200.zip


done

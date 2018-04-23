#!/bin/bash
ol=0
while true #run indefinitely
do
        inotifywait -r -e modify /var/log/com.log &&
        echo $ol
        ln=$(cat /var/log/com.log | wc -l)
        nl=$((ln-ol))
        awk "NR >=$ol && NR <=$ln" /var/log/com.log | awk '{ s = ""; for (i = 14; i <= NF; i++) s = s $i " "; print $10"\t"$3"\t"$8"\t"$6"\t"$12"\t"s}' > /var/log/mlog
        ol=$((ln+1))
	/root/Desktop/trap/logs_dump_to_mongo.py
done

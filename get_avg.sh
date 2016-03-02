#!/bin/bash

file=$1
previous=0
job_total=0
numlines=$(cat $file | wc -l)
linecount=0
all_total=0
job_count=1
while read line
  do
    time=$(echo $line | awk {'print $1}' | cut -d ',' -f 1)
    value=$(echo $line | awk '{print $2}' | cut -d ',' -f 1)
    if [[ $time -ge $previous ]]
      then
        job_total=$(($job_total+$value))
        previous=$time
        linecount=$(($linecount+1))
    else
        avg=$(($job_total/$linecount))
        echo "Job $job_count IOPS avg: $avg"
        all_total=$(($all_total+$avg))
        job_total=0
        linecount=0
        previous=0
        job_count=$(($job_count+1))
    fi
done < $file
echo "Job $job_count IOPS avg: $avg"
all_total=$(($all_total+$avg))
echo "Total IOPS: $(($all_total))"

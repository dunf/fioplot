#!/bin/bash

# fio.bash /my_test_Dir_or_Device hw testname dest_dir

# all data is stored in a /data directory which should exist

if [[ "$#" -ne 3 ]]; then
    echo "Illegal number of parameters"
    exit 1
fi

if [[ ! $1 =~ ^/.+ ]]; then
    echo "Please provide FULL PATH directory (where REALLYBIGFILE104 exists if this is a dir and not device)"
    exit 1
fi

if [[ ! -d /data ]]; then
    echo "/data does not exist!"
    exit 1
fi

if [[ ! -e /usr/bin/fio ]]; then
    echo "can't find exec /usr/bin/fio"
    exit 1
fi

if [[ "$EUID" -ne 0 ]]
  then echo "Please run as root"
  exit 1
fi

dirordev=$1
hw=$2
testname=$3
dest_dir=$4
runtime=60   # in seconds
ramptime=45   # in seconds
#filesize=32G  # filesize for fallocate


if [[ "$dest_dir" ne '' ]]; then
  temp_dir=/${dest_dir}/${hw}/${testname}/$(awk -v p=$$ 'BEGIN { srand(); s = rand(); \
   sub(/^0./, "", s); printf("%X_%X", p, s) }')
  mkdir -p "$temp_dir" || { echo '!! unable to create a tempdir' >&2; \
     temp_dir=; exit 1; }
else
  temp_dir=/data/${hw}/${testname}/$(awk -v p=$$ 'BEGIN { srand(); s = rand(); \
 43    sub(/^0./, "", s); printf("%X_%X", p, s) }')
fi

if [[ -d $dirordev ]]; then
  cd $dirordev
  # create huge file to test against
  filename="$(pwd)/REALLYBIGFILE104"
  if [[ ! -f $filename ]]; then
    echo "$filename does not exist!"
    exit 1
  fi
# fallocate -l $filesize $filename
elif [[ -b $dirordev ]]; then
  filename=$dirordev
else
  echo "$dirordev is not directory or device"
  exit
fi


cd $temp_dir

for jobs in 1 16 32 64 128
  do
    for depth in 1 # 16 32 64
      do
        echo " Doing $jobs jobs with depth $depth"
        name=fsrandR${jobs}-${depth}
        sync && echo 3 > /proc/sys/vm/drop_caches
        fio --filename=$filename --direct=1 --rw=randread --refill_buffers --norandommap \
        --randrepeat=0 --ioengine=libaio --bs=4k --iodepth=$depth \
        --numjobs=$jobs --runtime=$runtime --log_avg_msec=1000 --write_iops_log=${name}-iopslog \
        --write_bw_log=${name}-bwlog \
        --ramp_time=$ramptime --name=$name  > $temp_dir/$name
    done
done


echo "Random write"
for jobs in 1 16 32 64 128
  do
    for depth in 1 #16 32 64
      do
        echo " Doing $jobs jobs with depth $depth"
        name=fsrandW${jobs}-${depth}
        sync && echo 3 > /proc/sys/vm/drop_caches
        fio --filename=$filename --direct=1 --rw=randwrite --refill_buffers --norandommap \
        --randrepeat=0 --ioengine=libaio --bs=4k --iodepth=$depth \
        --numjobs=$jobs --runtime=$runtime --log_avg_msec=1000 --write_iops_log=${name}-iopslog \
        --write_bw_log=${name}-bwlog \
        --ramp_time=$ramptime --name=$name  > $temp_dir/$name
     done
done

exit 0

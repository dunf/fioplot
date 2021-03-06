#!/bin/bash

# fio.bash /my_test_Dir_or_Device hw testname dest_dir

# all data is stored in a /data directory which should exist

#if [[ "$#" -ne 3 ]]; then
#    echo "Illegal number of parameters"
#    exit 1
#fi

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
runtime=120   # in seconds
ramptime=60   # in seconds
#filesize=32G  # filesize for fallocate


if [[ -n $dest_dir ]]; then
  temp_dir=/${dest_dir}/${hw}/${testname}/$(awk -v p=$$ 'BEGIN { srand(); s = rand(); \
  sub(/^0./, "", s); printf("%X_%X", p, s) }')
  mkdir -p "$temp_dir" || { echo '!! unable to create a tempdir' >&2; \
     temp_dir=; exit 1; }
else
  temp_dir=/data/${hw}/${testname}/$(awk -v p=$$ 'BEGIN { srand(); s = rand(); \
  sub(/^0./, "", s); printf("%X_%X", p, s) }')
  mkdir -p "$temp_dir" || { echo '!! unable to create a tempdir' >&2; \
     temp_dir=; exit 1; }
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
starttime=$(date +"%s")
echo "Cephios testsuite started at $(date +"%T")"

echo "Sequential read bs=256K, no ramp_time"
jobs=1
depth=16
name=fsseqR${jobs}-${depth}
sync && echo 3 > /proc/sys/vm/drop_caches
fio --filename=$filename --direct=1 --rw=read --refill_buffers --ioengine=libaio \
--bs=256k --iodepth=$depth --numjobs=$jobs --runtime=$runtime  \
--write_iops_log=${name}-iopslog --log_avg_msec=1000 \
--name=$name  > $temp_dir/$name


echo "Sequential write bs=256K, no ramp_time"
jobs=1
depth=16
name=fsseqW${jobs}-${depth}
sync && echo 3 > /proc/sys/vm/drop_caches
fio --filename=$filename --direct=1 --rw=write --refill_buffers --ioengine=libaio \
--bs=256k --iodepth=$depth --numjobs=$jobs --runtime=$runtime \
--write_iops_log=${name}-iopslog --log_avg_msec=1000 \
--name=$name  > $temp_dir/$name


echo "Random read"
for jobs in 1 16
  do
    for depth in 1 16 32 64
      do
        echo " Doing $jobs jobs with depth $depth"
        name=fsrandR${jobs}-${depth}
        sync && echo 3 > /proc/sys/vm/drop_caches
        fio --filename=$filename --direct=1 --rw=randread --refill_buffers --norandommap \
        --randrepeat=0 --ioengine=libaio --bs=4k --iodepth=$depth \
        --numjobs=$jobs --runtime=$runtime --write_iops_log=${name}-iopslog \
        --log_avg_msec=1000 \
        --ramp_time=$ramptime --name=$name  > $temp_dir/$name
    done
done


echo "Random write"
for jobs in 1 16
  do
    for depth in 1 16 32 64
      do
        echo " Doing $jobs jobs with depth $depth"
        name=fsrandW${jobs}-${depth}
        sync && echo 3 > /proc/sys/vm/drop_caches
        fio --filename=$filename --direct=1 --rw=randwrite --refill_buffers --norandommap \
        --randrepeat=0 --ioengine=libaio --bs=4k --iodepth=$depth \
        --numjobs=$jobs --runtime=$runtime --write_iops_log=${name}-iopslog \
        --log_avg_msec=1000 \
        --ramp_time=$ramptime --name=$name  > $temp_dir/$name
     done
done


# Combined workload from Storage Review
# http://www.storagereview.com/fio_flexible_i_o_tester_synthetic_benchmark
echo "Mixed 70/30 random read and write with 8K block size"
jobs=16
depth=16
name=fsmixedRW7030${jobs}-${depth}
sync && echo 3 > /proc/sys/vm/drop_caches
fio --filename=$filename --direct=1 --rw=randrw --refill_buffers --norandommap \
--randrepeat=0 --ioengine=libaio --bs=8k --rwmixread=70 --iodepth=$depth \
--unified_rw_reporting=1 --numjobs=$jobs --runtime=$runtime \
--write_iops_log=${name}-iopslog --log_avg_msec=1000 \
--ramp_time=$ramptime --name=$name  > $temp_dir/$name

p=$(pwd)
cd $tempdir
bash gnuplot.sh $3
cd $p

echo "Cephios testsuite finished at $(date +"%T")"
finishtime=$(date +"%s")
elapsed=$((finishtime-starttime))
echo "Testsuite took $(($elapsed/60)) minutes and $((elapsed%60)) seconds..."

exit 0

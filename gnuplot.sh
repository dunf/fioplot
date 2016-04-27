#!/bin/bash

for var in $@
  do
    cd "$var"
    cd $(ls)
    mkdir png
    fio2gnuplot -d png -i -g
    cd ../../
done

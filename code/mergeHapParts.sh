#! /bin/bash

# Script to merge the part files (hap.gz) generate by the convert script.

inPrefix=$1
numParts=$2
outname=$3
suffix=$RANDOM

paste -d "" <(gunzip -c $inPrefix.part0.haps.gz) <(gunzip -c $inPrefix.part1.haps.gz) > $outname
for part in $(seq 2 $numParts); do
  paste $outname <(gunzip -c $inPrefix.part${part}.haps.gz) > temp.hap.$suffix
  mv temp.hap.suffix $outname
  echo $part merged
done

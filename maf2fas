#!/bin/bash
while read line
do
  arr=(${line// / })
  #echo ${arr[0]}
  python3 mafToFasta.py "sepgenes/${arr[3]}.maf" "sepgenes/${arr[3]}.fas"
done < Herato_chr2_filtered_290.bed

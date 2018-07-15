#!/bin/bash
while read line
do
  arr=(${line// / })
  echo ${arr[3]}
  python3 mafToFasta.py "sepgenes/${arr[3]}.maf" "sepgenes/${arr[3]}.fas"
done < Herato_chr2_modified.bed

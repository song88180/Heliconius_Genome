#!/bin/bash
#!/usr/bin/bash
dir="sepgenes/filtered"
while read line;
do
  arr=(${line// / })
  #echo ${arr[3]}
  if [ -f "${dir}/${arr[3]}_filtered.fas" ]; then
    /usr/bin/mafft  --globalpair --maxiterate 16 --reorder ${dir}/${arr[3]}_filtered.fas > ${dir}/${arr[3]}_realigned.fas
  fi
done < Herato_chr2_modified.bed

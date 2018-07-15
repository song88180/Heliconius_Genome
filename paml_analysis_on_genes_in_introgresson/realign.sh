#!/usr/bin/bash
while read line
do
  arr=(${line// / })
  #echo ${arr[3]}
  /usr/bin/mafft  --globalpair --maxiterate 16 --reorder sepgenes/${arr[3]}_filtered.fas > sepgenes/${arr[3]}_realigned.fas
done < Herato_chr2_filtered_290.bed

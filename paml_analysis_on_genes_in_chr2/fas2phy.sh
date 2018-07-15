#!/bin/bash
#!/usr/bin/bash
DIR="sepgenes/phylip"
while read line
do
  arr=(${line// / })
  echo ${arr[0]}
  python FastaToPhylip.py ${DIR}/${arr[0]} ${DIR}/${arr[0]}.phy
done < goodfas.list

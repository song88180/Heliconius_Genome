#!/bin/bash
DIR="sepgenes/realigned"
while read line; do
arr=(${line// / })
if [ "${arr[1]}" == '-' ]; then
    msa_view -V ${DIR}/${arr[0]} > ${DIR}/${arr[0]}.RC
    echo $line
fi
done < goodfas.list

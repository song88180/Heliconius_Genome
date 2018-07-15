#!/bin/bash
while read line; do
rm ${line}_filtered.fas
echo ${line}_filtered.fas
done < ../../removed.list

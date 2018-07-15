#!/bin/bash
while read line
do
Out=`echo $line | sed 's/\.phy//'`
omega=`grep "w (dN/dS) for branches:" ${Out}/mlc | awk '{print $5","$6}'` # this is for 2-ratio results
#omega=`grep "omega (dN/dS)" ${Out}/mlc | awk '{print $4}'`  #this is for 1-ratio results
lnL=`grep "lnL(" ${Out}/mlc | awk '{print $5}'`
Out=$Out','$omega','$lnL
echo $Out
echo $Out >> two-ratio.csv
done < namelist

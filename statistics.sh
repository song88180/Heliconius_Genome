#!/bin/bash
while read line
do
Out=`echo $line | sed 's/\.phy//'`
omega=`grep "w (dN/dS) for branches:" ${dir}/mlc | awk '{print $5","$6}'` . # this is for 2-ratio results
#omega=`grep "omega (dN/dS)" ${dir}/mlc | awk '{print $4}'`  #this is for 1-ratio results
lnL=`grep "lnL(" ${dir}/mlc | awk '{print $5}'`
Out=$Out','$omega','$lnL
echo $Out >> statistics
done < namelist

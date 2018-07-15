#!/bin/bash
#ls *.phy > namelist
while read line
do
#arr=(${line// / })
name=`echo ${line} | sed 's/\.phy//'`
#mkdir $name
#mv $line $name
#sed "1s/seqfile =/seqfile = ${name}\/${line}/;3s/outfile =/outfile = ${name}\/mlc/" codeml.ctl > ${name}/codeml.ctl
echo | codeml ${name}/codeml.ctl   # when running codeml, it requires you to press enter to continue, thus "echo |" is added to input '\n'
if [[ "$?" != "0" ]];then
  echo "${line}\n" >> failed.log
fi
done < namelist

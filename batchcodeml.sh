#!/bin/bash
#ls *.phy > namelist
while read line
do
dir=`echo $line | sed 's/\.phy//'`
mkdir $dir
mv $line $dir
sed "1s/seqfile =/seqfile = ${dir}\/$line/;3s/outfile =/outfile = ${dir}\/mlc/" codeml.ctl > ${dir}/codeml.ctl
echo | codeml ${dir}/codeml.ctl   # when running codeml, it requires you to press enter to continue, thus "echo |" is added to input '\n'
if [[ "$?" != "0" ]];then
  echo "${line}\n" >> failed.log
fi
done < namelist

#!/bin/bash
#(Hsar Hdem Htel)(Hhsa HeraRef Hhim)
while read line
do
  arr=(${line// / })
  sed -n '/>Hsar/{p;n;p};/>Hdem/{p;n;p};/Htel/{p;n;p};/>Hhsa/{p;n;p};/>HeraRef/{p;n;p};/>HeraDisco/{p;n;p};/>Hhim/{p;n;p}' sepgenes/${arr[3]}.fas > sepgenes/${arr[3]}_filtered.fas
  num=`grep ">Hsar\|>Hdem\|>Htel\|>Hhsa\|>HeraRef\|>HeraDisco\|>Hhim" sepgenes/${arr[3]}_filtered.fas | wc -l`
  if [ "$num" -ne 7 ]; then
    echo "${arr[3]}:$num:removed"
    rm sepgenes/${arr[3]}_filtered.fas
  fi
done < Herato_chr2_modified.bed

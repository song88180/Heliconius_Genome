#!/bin/bash
refGenome="HeraRef"
halFile="finalAssemblies_highQual_1kbFilter_161101.hal"
while read line
do
  arr=(${line// / })
  echo $line > sepgenes/${arr[3]}.bed
  inFile="sepgenes/${arr[3]}.bed"
  mafFile="sepgenes/${arr[3]}.maf"
  hal2maf  --noAncestors --noDupes --onlyOrthologs --refGenome $refGenome --refTargets $inFile $halFile $mafFile
done < Herato_chr2_filtered_290.bed

#!/bin/bash
while read line
do
hal2fasta --sequence $line ../../finalAssemblies_highQual_1kbFilter_161101.hal Hsar >> Hsar_refgenome.fas
done < Hsarseqlist

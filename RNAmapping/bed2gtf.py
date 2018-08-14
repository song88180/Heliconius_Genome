#!/usr/bin/python
import pandas as pd
File = "Hsar_chr2_nodupe_290.bed"
BED = pd.read_table(File,header=None)
for i in range(0,BED[0].size):
    seq_name = BED.iloc[i][0]
    start = BED.iloc[i][1]
    exon_length = list(map(int, BED.iloc[i][10].split(',')))
    exon_start = list(map(int, BED.iloc[i][11].split(',')))
    exon_num = len(exon_start)
    strand = BED.iloc[i][5]
    transcript_id = BED.iloc[i][3]
    for j in range(0,exon_num):
        gff_start = start + exon_start[j]+1;
        gff_end = gff_start + exon_length[j];
        print("%s\t.\texon\t%d\t%d\t.\t%s\t.\ttranscript_id \"%s\"; gene_id \"%s\"; gene_name \"%s\";"%(seq_name,gff_start,gff_end,strand,transcript_id,transcript_id, transcript_id))

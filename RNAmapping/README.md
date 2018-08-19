Download sra file from NCBI:

    Hsar_leg_1  ->	ERR841723.sra
    Hsar_leg_2  ->	ERR841715.sra
    Hera_leg_1  ->  ERR841719.sra
    Hera_leg_2  ->	ERR841714.sra

Convert sra file to fastq file:

    fastq-dump --split-3 --gzip *.sra

Plan to use bwa to map reads at first:

    bwa mem -t 12 Herato_chr_all.fas fastq/Hera_leg_2_1.fastq.gz fastq/Hera_leg_2_2.fastq.gz | gzip -3 > Hera_leg_2.sam.gz
    bwa mem -t 12 Herato_chr_all.fas fastq/Hera_leg_1_1.fastq.gz fastq/Hera_leg_1_2.fastq.gz | gzip -3 > Hera_leg_1.sam.gz
    bwa mem -t 12 Herato_chr_all.fas fastq/Hsar_leg_1_1.fastq.gz fastq/Hsar_leg_1_2.fastq.gz | gzip -3 > Hsar_leg_1.sam.gz
    bwa mem -t 12 Herato_chr_all.fas fastq/Hsar_leg_2_1.fastq.gz fastq/Hsar_leg_2_2.fastq.gz | gzip -3 > Hsar_leg_2.sam.gz

Then found tophat is more suitbale, so re-run the mapping using tophat with transcriptome annotation gtf:

    bowtie2-build --threads 12 Hera_0211-14.fa

    tophat2 -o Hera_0211-14_1_tophat2 -p 12 -G refgenome/Hera_0211-14.gtf refgenome/Hera_0211-14 fastq/Hera_leg_1_1.fastq.gz fastq/Hera_leg_1_2.fastq.gz
    tophat2 -o Hera_0211-14_2_tophat2 -p 12 -G refgenome/Hera_0211-14.gtf refgenome/Hera_0211-14 fastq/Hsar_leg_2_1.fastq.gz fastq/Hsar_leg_2_2.fastq.gz
    tophat2 -o Hsar_0211-14_1_tophat2 -p 12 -G refgenome/Hera_0211-14.gtf refgenome/Hera_0211-14 fastq/Hsar_leg_1_1.fastq.gz fastq/Hsar_leg_1_2.fastq.gz
    tophat2 -o Hsar_0211-14_2_tophat2 -p 12 -G refgenome/Hera_0211-14.gtf refgenome/Hera_0211-14 fastq/Hsar_leg_2_1.fastq.gz fastq/Hsar_leg_2_2.fastq.gz

Mapping reads alignments to gene annotation:

    stringtie -p 2 -G ../refgenome/Hera_0211-14.gtf -o Hera_leg_1_0211-14.gtf -l Hera_leg_1_0211-14 Hera_leg_1_0211-14.bam
    stringtie -p 2 -G ../refgenome/Hera_0211-14.gtf -o Hera_leg_2_0211-14.gtf -l Hera_leg_2_0211-14 Hera_leg_2_0211-14.bam
    stringtie -p 2 -G ../refgenome/Hera_0211-14.gtf -o Hsar_leg_1_0211-14.gtf -l Hsar_leg_1_0211-14 Hsar_leg_1_0211-14.bam
    stringtie -p 2 -G ../refgenome/Hera_0211-14.gtf -o Hsar_leg_2_0211-14.gtf -l Hsar_leg_2_0211-14 Hsar_leg_2_0211-14.bam

 Merge gtf for the following DEG analysis:

    stringtie --merge -p 2 -G ../refgenome/Hera_0211-14.gtf -o HeraHsar_merged.gtf gtflist.txt
    
Calculate normalized expression abundance using merged gtf:
    
    stringtie -e -p 2 -G HeraHsar_merged.gtf -A Hera_leg_1_0211-14_genes.gtf -o Hera_leg_1_0211-14_transcripts.gtf ../bam/Hera_leg_1_0211-14.bam
    stringtie -e -p 2 -G HeraHsar_merged.gtf -A Hera_leg_2_0211-14_genes.gtf -o Hera_leg_2_0211-14_transcripts.gtf ../bam/Hera_leg_2_0211-14.bam
    stringtie -e -p 2 -G HeraHsar_merged.gtf -A Hsar_leg_1_0211-14_genes.gtf -o Hsar_leg_1_0211-14_transcripts.gtf ../bam/Hsar_leg_1_0211-14.bam
    stringtie -e -p 2 -G HeraHsar_merged.gtf -A Hsar_leg_2_0211-14_genes.gtf -o Hsar_leg_2_0211-14_transcripts.gtf ../bam/Hsar_leg_2_0211-14.bam

Generate reads count table (for DESeq2) using merged gtf and bam:

    htseq-count -q -f bam -s no -i transcript_id Hera_leg_1_0211-14.bam ../gtf_merged/HeraHsar_merged.gtf > Hera_leg_1_0211-14.count
    htseq-count -q -f bam -s no -i transcript_id Hera_leg_2_0211-14.bam ../gtf_merged/HeraHsar_merged.gtf > Hera_leg_2_0211-14.count
    htseq-count -q -f bam -s no -i transcript_id Hsar_leg_1_0211-14.bam ../gtf_merged/HeraHsar_merged.gtf > Hsar_leg_1_0211-14.count
    htseq-count -q -f bam -s no -i transcript_id Hsar_leg_2_0211-14.bam ../gtf_merged/HeraHsar_merged.gtf > Hsar_leg_2_0211-14.count
    
    join Hera_leg_1_0211-14.count Hera_leg_2_0211-14.count | join - Hsar_leg_1_0211-14.count | join - Hsar_leg_2_0211-14.count > counttable.txt
    
Generate heat map using fpkm:

    join -t $'\t' Hera_leg_1_0211-14_TID.gtf Hera_leg_2_0211-14_TID.gtf | join -t $'\t' - Hsar_leg_1_0211-14_TID.gtf | join -t $'\t' - Hsar_leg_2_0211-14_TID.gtf > out_fpkm.gtf
    
    
------------------------------------------

liftOver HeraRef annotation to Hsar genome:

    halLiftover --noDupes <halFile> HeraRef Herato_chr2_nodupe_290.bed Hsar Hsar_chr2_nodupe_290.bed
    
convert BED to GTF:

    python bed2gtf.py Hsar_chr2_nodupe_290.bed | sort -t $'\t' -k1,1 -k4,4n > Hsar_sorted_refgenome.gtf
    
Get Hsar Fasta sequence:

    awk '{print $1}' Hsar_sorted_refgenome.gtf | uniq > Hsarseqlist
    getFasta.sh
    
Redo RNA mapping using new generated Hsar GTF & Fasta. (Same procedures as above)

Filter reads that have mapping quality over 50:

    samtools view -b -q 50 -o <output.bam> accepted_hits.bam 

Results Comparism:

| | Hera map to Hera 1 | Hera map to Hera 2 | Hsar map to Hera 1 | Hsar map to Hera 2 | Hsar map to Hsar 1 | Hsar map to Hsar 2 |
| - | - | - | - | - | - | - |
| annotation number (gtf) | 122 | 122 | 122 | 122 | 116 | 116 |
| exon alignment length (bp) | 167745 | 167745 | 167745 | 167745 | 139018 | 139018 |
| mapped | 150780 | 47339 | 18213 | 37362 | 63436 | 103883 |
| properly paired | 62880 | 17970 | 5114 | 11028 | 37052 | 49866 |
| unmapped | 19754743 | 18089251 | 11844181 | 24629228 | 11803455 | 24576283 |
| mapped MQ=50 | 104922 | 32062 | 14881 | 30599 | 54576 | 80793 |
| properly paired MQ=50 | 61606 | 17602 | 5086 | 10974 | 36758 | 49280 |

------------------------------------------

Extract single copy orthologs from maf file:

    hal2maf  --noAncestors --noDupes --onlyOrthologs --refGenome HeraRef --refTargets Hera_chr2_nodupe_290.bed --targetGenomes "HeraRef,Hsar" ../../../finalAssemblies_highQual_1kbFilter_161101.hal HerHsar_chr2_inv.maf
    python getSingleCopy.py  HeraHsar_chr2_inv.maf
    maf-convert axt HeraHsar_chr2_inv_singleCopy.maf > HeraHsar_chr2_inv_singleCopy.axt
    
Only 1 sequence has multiple copy. looking at the alignment, it should be a single copy orthologs...

    a
    s       HeraRef.Herato_chr2_5   62260   187     +       3116133 TCATGAATTCGACGACGGCCCACAAGGCTTGGCCCCGTATCTTAGGGCTCTTAAGGCACCAGTACTGGCTGCAAACATGGACACCACCAAAGAACCCGTACTAAATGGACTATACAGGCCTCATGTTATTATAGAACGAAACAAGAGGAGAATTGGTCTAATTGGACTAATTACTACTGATACTAAG
    s       Hsar.EI_a_scaffold_17978        958     186     -       20716   CCATGAATTCGATGATGGAATAGCGGGCCTCGCACCATACCTTGCGGCACTCCAAGCTCCTGTTGTCGTTGCAAATATCAACACAACCCTTGAACCTAGTCTGAATGGTTTATACAAACCTCATATTGTGATACAAAGATACGGAAGAAAAATTGGAATAATTGGTCTTATAACGACAGAAACTAA-
    s       Hsar.EI_a_scaffold_19101        5023    1       -       37284   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------A
    
    

extracts constitutive exons from gff file:

    exon_utils --get-const-exons Hera_chr2_inv.gff --min-exon-size=100 --output-dir exons/

656 out of 1195 exons remained.

    perl gffToChrs.pl exons/Hera_chr2_inv.min_100.const_exons.gff gffChrs/
    sort -t $'\t' -k4,4n Herato_chr2_X.gff > Herato_chr2_X_sorted.gff
    
    
Liftover Hera annotation to Hsar genome:
    
    perl axtLift.pl gffChrs/Herato_chr2_X_sorted.gff axtChrs/HeraHsar_chr2_X.axt HsarGff
    
451 out of 656 exons liftover to Hsar genome.
    
merge.sh:

    ls -1 Hsar* > Hsar_gff.list
    while read file;do
        sort -t $'\t' -k4,4n $file >> Hsar_inv_merged.gff
    done < Hsar_gff.list
    
    gffread Hera_chr2_inv_sorted.gff -T -o Hera_chr2_inv_sorted.gtf
    gffread Hsar_liftover.gff -T -o Hsar_liftover_sorted.gtf
    
Then use the new generated GTF file to repeat the RNA reads mapping as above.
    
    

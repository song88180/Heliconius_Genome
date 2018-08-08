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

Generate reads count table (for DESeq2) using merged gtf and bam. 

    htseq-count -q -f bam -s no -i transcript_id Hera_leg_1_0211-14.bam ../gtf_merged/HeraHsar_merged.gtf > Hera_leg_1_0211-14.count
    htseq-count -q -f bam -s no -i transcript_id Hera_leg_2_0211-14.bam ../gtf_merged/HeraHsar_merged.gtf > Hera_leg_2_0211-14.count
    htseq-count -q -f bam -s no -i transcript_id Hsar_leg_1_0211-14.bam ../gtf_merged/HeraHsar_merged.gtf > Hsar_leg_1_0211-14.count
    htseq-count -q -f bam -s no -i transcript_id Hsar_leg_2_0211-14.bam ../gtf_merged/HeraHsar_merged.gtf > Hsar_leg_2_0211-14.count
    join Hera_leg_1_0211-14.count Hera_leg_2_0211-14.count | join - Hsar_leg_1_0211-14.count | join - Hsar_leg_2_0211-14.count > counttable.txt
    
Generate heat map using fpkm

    join -t $'\t' Hera_leg_1_0211-14_TID.gtf Hera_leg_2_0211-14_TID.gtf | join - Hsar_leg_1_0211-14_TID.gtf | join - Hsar_leg_2_0211-14_TID.gtf > out_fpkm.gtf
    
    

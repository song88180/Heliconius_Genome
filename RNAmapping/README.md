Download sra file from NCBI:

    Hsar_leg_1  ->	ERR841723.sra
    Hsar_leg_2  ->	ERR841715.sra
    Hera_leg_1  ->  ERR841719.sra
    Hera_leg_2  ->	ERR841714.sra

convert sra file to fastq file:

    fastq-dump --split-3 --gzip *.sra

Plan to use bwa to map reads at first:

    bwa mem -t 12 Herato_chr_all.fas fastq/Hera_leg_2_1.fastq.gz fastq/Hera_leg_2_2.fastq.gz | gzip -3 > Hera_leg_2.sam.gz
    bwa mem -t 12 Herato_chr_all.fas fastq/Hera_leg_1_1.fastq.gz fastq/Hera_leg_1_2.fastq.gz | gzip -3 > Hera_leg_1.sam.gz
    bwa mem -t 12 Herato_chr_all.fas fastq/Hsar_leg_1_1.fastq.gz fastq/Hsar_leg_1_2.fastq.gz | gzip -3 > Hsar_leg_1.sam.gz
    bwa mem -t 12 Herato_chr_all.fas fastq/Hsar_leg_2_1.fastq.gz fastq/Hsar_leg_2_2.fastq.gz | gzip -3 > Hsar_leg_2.sam.gz

Then found tophat is more suitbale, so re-run the mapping using tophat with transcriptome annotation gtf:

    tophat2 -o Hera_0211-14_1_tophat2 -p 12 -G refgenome/Hera_0211-14.gtf refgenome/Hera_0211-14 fastq/Hera_leg_1_1.fastq.gz fastq/Hera_leg_1_2.fastq.gz
    tophat2 -o Hera_0211-14_2_tophat2 -p 12 -G refgenome/Hera_0211-14.gtf refgenome/Hera_0211-14 fastq/Hsar_leg_2_1.fastq.gz fastq/Hsar_leg_2_2.fastq.gz
    tophat2 -o Hsar_0211-14_1_tophat2 -p 12 -G refgenome/Hera_0211-14.gtf refgenome/Hera_0211-14 fastq/Hsar_leg_1_1.fastq.gz fastq/Hsar_leg_1_2.fastq.gz
    tophat2 -o Hsar_0211-14_2_tophat2 -p 12 -G refgenome/Hera_0211-14.gtf refgenome/Hera_0211-14 fastq/Hsar_leg_2_1.fastq.gz fastq/Hsar_leg_2_2.fastq.gz

mapping reads alignments to gene annotation:

    stringtie -p 2 -G ../refgenome/Hera_0211-14.gtf -o Hera_leg_1_0211-14.gtf -l Hera_leg_1_0211-14 Hera_leg_1_0211-14.bam
    stringtie -p 2 -G ../refgenome/Hera_0211-14.gtf -o Hera_leg_2_0211-14.gtf -l Hera_leg_2_0211-14 Hera_leg_2_0211-14.bam
    stringtie -p 2 -G ../refgenome/Hera_0211-14.gtf -o Hsar_leg_1_0211-14.gtf -l Hsar_leg_1_0211-14 Hsar_leg_1_0211-14.bam
    stringtie -p 2 -G ../refgenome/Hera_0211-14.gtf -o Hsar_leg_2_0211-14.gtf -l Hsar_leg_2_0211-14 Hsar_leg_2_0211-14.bam
    

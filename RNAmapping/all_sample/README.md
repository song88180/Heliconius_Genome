Download sra file from NCBI:

    prefetch <SRAfile>

    ERR841719   ->    Hera_leg_1
    ERR841714   ->    Hera_leg_2
    ERR841735   ->    Hera_mouth_1
    ERR841732   ->    Hera_mouth_2
    ERR841718   ->    Hera_antennae_1
    ERR841724   ->    Hera_antennae_2
    ERR841723   ->    Hsar_leg_1
    ERR841715   ->    Hsar_leg_2
    ERR841731   ->    Hsar_mouth_1
    ERR841722   ->    Hsar_mouth_2
    ERR841728   ->    Hsar_antennae_1
    ERR841733   ->    Hsar_antennae_2

Convert sra file to fastq file:
    
    fastq-dump --split-3 --gzip *.sra

Extract single copy orthologs from maf file:

    hal2maf  --noAncestors --noDupes --onlyOrthologs --refGenome HeraRef --refTargets Hera_hal_chr2.bed --targetGenomes "HeraRef,Hsar" ../data/finalAssemblies_highQual_1kbFilter_161101.hal HerHsar_chr2_inv.maf
    python getSingleCopy.py  HeraHsar_chr2_inv.maf
    maf-convert axt HeraHsar_chr2_inv_singleCopy.maf > HeraHsar_chr2_inv_singleCopy.axt

alignments: 7403 -> 6356 (single copy)

extracts constitutive exons from gff file:

    exon_utils --get-const-exons Hera_hal_chr2.gff --min-exon-size=100 --output-dir exons/
    (out put file: Hera_hal_chr2.min_100.const_exons.gff -> Hera_hal_chr2_filtered.gff)

6027  -> 3098 (constitutive)

Liftover Hera annotation to Hsar genome:

    perl axtLift.pl gffChrs/Herato_chr2_X_sorted.gff axtChrs/HeraHsar_chr2_X.axt HsarGff

3098 -> 2091(Liftover)

Merge all generated GFF using merge.sh:

    ls -1 Hsar* > Hsar_gff.list
    while read file;do
        sort -t $'\t' -k4,4n $file >> Hsar_liftover_sorted.gff
    done < Hsar_gff.list
    
It seems tophat only recognize GTF (weird, should be able to use GFF), thus convert GFF to GTF:

    gffread Hsar_liftover_sorted.gff -T -o Hsar_liftover_sorted.gtf
    gffread Hera_hal_chr2_filtered.gff -T -o Hera_hal_chr2_filtered.gtf

(remember to check if the scaffold names in GTF and FASTA are the same. In this experiment, scaffold names of Hsar in GTF is "Hsar.EI_a_scaffold_11473", while in FASTA "EI_a_scaffold_11473")

Map using tophat with transcriptome annotation gtf:

    bowtie2-build --threads 12 Hsar_hal_from_Hera_chr2.fas Hsar_hal_from_Hera_chr2
    bowtie2-build --threads 12 Hera_hal_chr2.fas Hera_hal_chr2
    
    tophat2 -o Hsar_hal_[leg,mouth,antennae]_[1,2] -p 12 -G refgenome/gtf/Hsar_liftover_sorted.gtf refgenome/fas/Hsar_hal_from_Hera_chr2 fastq/Hsar_[leg,mouth,antennae]_[1,2]_1.fastq.gz fastq/Hsar_[leg,mouth,antennae]_[1,2]_2.fastq.gz
    tophat2 -o Hera_hal_[leg,mouth,antennae]_[1,2] -p 12 -G refgenome/gtf/Hera_hal_chr2_filtered.gtf refgenome/fas/Hera_hal_chr2 fastq/Hera_[leg,mouth,antennae]_[1,2]_1.fastq.gz fastq/Hera_[leg,mouth,antennae]_[1,2]_2.fastq.gz 


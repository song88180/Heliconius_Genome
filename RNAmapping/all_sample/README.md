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

Generate reads count table (for DESeq2) using GTF and BAM:

    htseq-count -q -f bam -s no -i transcript_id Hera_hal_[leg,mouth,antennae]_[1,2]/accepted_hits.bam refgenome/gtf/Hera_hal_chr2_filtered.gtf > count/Hera_hal_[leg,mouth,antennae]_chr2_[1,2].count
    htseq-count -q -f bam -s no -i transcript_id Hsar_hal_[leg,mouth,antennae]_[1,2]/accepted_hits.bam refgenome/gtf/Hsar_liftover_sorted.gtf > count/Hsar_hal_[leg,mouth,antennae]_chr2_[1,2].count
    
    join Hera_hal_leg_chr2_1.count Hera_hal_leg_chr2_2.count | join - Hera_hal_mouth_chr2_1.count | join - Hera_hal_mouth_chr2_2.count | join - Hera_hal_antennae_chr2_1.count | join - Hera_hal_antennae_chr2_2.count | join - Hsar_hal_leg_chr2_1.count | join - Hsar_hal_leg_chr2_2.count | join - Hsar_hal_mouth_chr2_1.count | join - Hsar_hal_mouth_chr2_2.count | join - Hsar_hal_antennae_chr2_1.count | join - Hsar_hal_antennae_chr2_2.count > counttable.txt
    
    
DEG analysis using R

-------------------------
# Results

### Liftover

| | original (include duplicates) | constitutive, >100bp | Liftover |
| - | - | - | - |
| exon | 6027 | 3098 | 2091 |
| gene | 777 | 552 | 419 |


### Mapping results

|                     |  unmapped |  mapped | properly paired |
|           -         |  -        |    -    |   -    |
| Hera_hal_leg_1      | 19631292  | 301086  | 142698 |
| Hera_hal_leg_2      | 18040029  | 107853  | 49540  |
| Hera_hal_mouth_1    | 19416856  | 127056  | 53540  |
| Hera_hal_mouth_2    | 20263657  | 374506  | 171650 |
| Hera_hal_antennae_1 | 18791891  | 548227  | 267276 |
| Hera_hal_antennae_2 | 18184117  | 88378   | 37644  |
| Hsar_hal_leg_1      | 11738685  | 127976  | 64010  |
| Hsar_hal_leg_2      | 24426099  | 252099  | 128408 |
| Hsar_hal_mouth_1    | 1198696   | 25443   | 15800  |
| Hsar_hal_mouth_2    | 13461659  | 217239  | 110388 |
| Hsar_hal_antennae_1 | 15974796  | 267501  | 140012 |
| Hsar_hal_antennae_2 | 14691409  | 210521  | 107052 |


### DEG results

gene number: 419 -> 325 (exclusion, sum(counts)>60) -> 106(significant difference) 

gene in Hera inversion : 127 

gene in rest of chr2 :  552-127=425

gene in Hera inversion after liftover sum(counts)>60: 73

gene in rest of chr2 after liftover: 325-73=252

significant difference gene in inversion: 28

significant difference gene in rest of chr2: 106-22=84


significant genes:

Hera < Hsar: 34

Hera > Hsar: 106-34=72

significant genes in inversion: 

Hera < Hsar: 5

Hera > Hsar: 28-5=23

| |  constitutive, >100bp | Liftover | sum(counts)>60 | significant difference |
| - | - | - | - | - |
| all genes | 552 | 419 | 325 | 106 |
| genes in inversion | 127 | ? | 73 | 28 |
| genes in rest of chr2 | 425 | ? | 252 | 84 | 
| ratio inv/rest | 0.30 | ? | 0.027 | 0.033 | 

| gene | Hera_leg_1 | Hera_leg_2 | Hera_mouth_1 | Hera_mouth_2 | Hera_antennae_1 | Hera_antennae_2 | Hsar_leg_1 | Hsar_leg_2 | Hsar_mouth_1 | Hsar_mouth_2 | Hsar_antennae_1 | Hsar_antennae_2 |
| - | - | - | - | - | - | - | - | - | - | - | - | - |
| evm.model.Herato0211.93 | 0 | 0 | 3 | 4 | 0 | 0 | 2 | 7 | 1 | 7 | 86 | 13 |
| evm.model.Herato0214.19 | 7 | 2 | 0 | 6 | 32 | 4 | 12 | 29 | 2 | 39 | 58 | 50 |
| evm.model.Herato0214.29.1 | 7 | 0 | 0 | 12 | 8 | 2 | 6 | 33 | 4 | 27 | 33 | 33 |
| evm.model.Herato0214.30 | 93 | 36 | 38 | 86 | 135 | 20 | 156 | 309 | 56 | 217 | 182 | 187 |
| evm.model.Herato0214.48 | 44 | 0 | 0 | 56 | 138 | 0 | 89 | 297 | 59 | 228 | 772 | 792 |

evm.model.Herato0214.30: Leucine-zipper-like transcriptional regulator 1

evm.model.Herato0214.48: Calmodulin 


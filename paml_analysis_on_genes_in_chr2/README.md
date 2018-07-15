# Heliconius_Genome
Heliconius_Genome_Project

Scripts need to be changed to fit your own environment!

Steps:
1. getmaf.sh
>create bed files for each of the genes (only have one line), run hal2maf against all the bed files to get individual maf file.
2. maf2fas.sh
>turn maf file to fasta alignment using mafToFasta.py
3. filterfas.sh
>only keep the sequences of the species of interest (Hsar,Hdem,Htel,Hhsa,HeraRef,Hhim) in the fasta alignment, and check if the alignment have all the species required, remove the file if not.
4. realign.sh
>realign fasta alignment using mafft, some of the file would fail to be realgined, those files are recorded in removed.list, remove those files using removed.sh.
5. goodfas.py
>verify if alignments have good quality, write filenames of alignments which have good (bad) quality into goodfas.list (badfas.list). The strand direction is detected at the same time.
6. revertfas.sh
>change the alignment to the reverse complementary if its strand is detected as '-'
7. fas2phy.py
>change fasta to phylip format using FastaToPhylip.py.
8. batchcodeml.sh
>make directory for each gene, move Phylip file and modified codeml.ctl to the file, run codeml for each gene.
9. statistics.sh
>extract w value and lnL value from PAML main results file (mlc).

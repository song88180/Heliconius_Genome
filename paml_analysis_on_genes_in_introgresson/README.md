# Heliconius_Genome
Heliconius_Genome_Project

Scripts need to be changed to fit your own environment!

Steps:
1. getindvmaf.sh 
>create bed files for each of the genes (only have one line), run hal2maf against all the bed files to get individual maf file.
2. maf2fas.sh
>turn maf file to fasta alignment.
3. filterfas.sh
>only keep the sequences of the species of interest (Hsar,Hdem,Htel,Hhsa,HeraRef,Hhim) in the fasta alignment, and check if the alignment have all the species required, remove the file if not.
4. use Geneious to view the alignments, export them as Phylip files
5. batchcodeml.sh
>make directory for each gene, move Phylip file and modified codeml.ctl to the file, run codeml for each gene.
6. statistics.sh
>extract w value and lnL value from PAML main results file (mlc).

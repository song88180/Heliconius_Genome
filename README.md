# Heliconius_Genome
Heliconius_Genome_Project

Steps:
1. getindvmaf.sh   # create bed files for each of the genes (only have one line), run hal2maf against all the bed files to get individual maf files.
2. maf2fas.sh     # turn maf file to fasta file.
3. filterfas.sh     #only keep the sequences of the species of interest (Hsar,Hdem,Htel,Hhsa,HeraRef,Hhim) in the fasta alignment, and check if the alignment have all the species required, remove the file if not.
5. use Geneious to view the alignments, export them as Phylip files
6. batchcodeml.sh

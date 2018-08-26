Get 4-fold degenerate sites in the inversion region:

    hal4dExtract finalAssemblies_highQual_1kbFilter_161101.hal HeraRef Herato_chr2_filtered_290.bed Herato_chr2_filtered_290.4d.bed
    (hal4dExtract $halfile $RefGenome $refTargets $output)
    
    hal2maf --noDupes --refGenome HeraRef --refTargets Herato_chr2_filtered_290.4d.bed --TargetGenomes "HeraRef,HeraDisco,Hhsa,Hsar,Hdem,Htel,Hhim,HmelRef,Etal" finalAssemblies_highQual_1kbFilter_161101.hal Herato_chr2_filtered_290.4d.maf
    
Generate neutral .mod file:

    phyloFit --tree inversion.tree --out-root Herato_chr2_filtered_290.4d --min-informative 1000 --msa-format MAF --init-random Herato_chr2_filtered_290.4d.maf
    
Get MAF file separate by scaffold:

    hal2maf --noDupes --refGenome HeraRef --refTargets Herato_chr2_filtered_scafX.bed --TargetGenomes "HeraRef,HeraDisco,Hhsa,Hsar,Hdem,Htel,Hhim,HmelRef,Etal" finalAssemblies_highQual_1kbFilter_161101.hal inv_scafX.maf
    
 dless analysis:
 
    dless -i MAF inv_scafX.maf Herato_chr2_filtered_290.4d.mod > inv_scafX_dlessOut.gff
 
 Match dless annotation of interest to potential corresponding genes, output summary file FindCorrGenes_scafX.csv:
 
    grep -E "Hhsa-HeraRef|Hhsa-HeraDisco|HeraRef-Hhsa|HeraDisco-Hhsa|Hhsa-Hhim|Hhim-Hhsa|Hsar-Htel|Htel-Hsar|Hdem-Htel|Htel-Hdem|" inv_scafX_dlessOut.gff > inv_scafX_dlessOut_filtered.gff
    python FindCorrGenes.py Herato_chr2_filtered_scafX.bed inv_scafX_dlessOut_filtered.gff > FindCorrGenes_scafX.result
    
Looking up GO term or other description for each genes from Lepbase, and add the infomation into previously generated FindCorrGenes_scafX.csv

http://ensembl.lepbase.org/Heliconius_erato_demophoon_v1/Info/Index

---------------------------

Results:

87 dless annotations in total, including 36 dless annotations from 26 genes, and  51 dless annotations from non-coding region. and it seems part of the genes are DNA/Protein/ion binding proteins, and have oxidation reduction functions. 
    
    

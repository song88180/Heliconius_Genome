Get 4-fold degenerate sites in the inversion region:

    hal4dExtract finalAssemblies_highQual_1kbFilter_161101.hal HeraRef Herato_chr2_filtered_290.bed Herato_chr2_filtered_290.4d.bed
    (hal4dExtract $halfile $RefGenome $refTargets $output)
    
    hal2maf --noDupes --refGenome HeraRef --refTargets Herato_chr2_filtered_290.4d.bed finalAssemblies_highQual_1kbFilter_161101.hal Herato_chr2_filtered_290.4d.maf
    
Generate .mod file:

    phyloFit --tree inversion.tree --out-root Herato_chr2_filtered_290.4d --min-informative 1000 --msa-format MAF --init-random Herato_chr2_filtered_290.4d.maf
    
    
    

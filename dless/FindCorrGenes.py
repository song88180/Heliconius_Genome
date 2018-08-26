#!/usr/bin/python3
import pandas as pd
import sys
def Position_to_exon(Gene,start,end):
    line=BED[BED[3].isin([Gene])]
    exonstart=line.iloc[0,11].split(',')[:-1]
    exonlen=line.iloc[0,10].split(',')[:-1]
    if line.iloc[0,5]=='-':
        start=line.iloc[0,2]-start
        end=line.iloc[0,2]-end
    else:
        start=start-line.iloc[0,1]
        end=end-line.iloc[0,1]
    for i in range(0,len(exonstart)):
        if int(exonstart[i]) > start:
            start1=int(exonstart[i-1])
            end1=int(exonlen[i-1])+start1
            start2=int(exonstart[i])
            end2=int(exonlen[i])+start2
            break
    if end < end1:
        return "exon"
    elif start < end1 and end > end1 and end < start2:
        exonratio=(end1-start)/(end1-start1)
        intronratio=(end1-start)/(end1-start1)
        if exonratio>0.6 and intronratio<0.1:
            return "exon"
        elif exonratio<0.1 and intronratio>0.6:
            return "intron"
        else:
            return "exon+intron"
    elif start < end1 and end > start2:
        exonratio1=(end1-start)/(end1-start1)
        exonratio2=(end-start2)/(end2-start2)
        intronratio=(start2-end1)/min((end1-start1),(end2-start2))
        if exonratio1<0.1 and exonratio2<0.1 and intronratio>0.6:
            return "intron"
        else:
            return "exon+intron"
    elif start > end1 and end < start2:
        return "intron"
    elif start > end1 and end > start2:
        exonratio=(end-start2)/(end2-start2)
        intronratio=(start2-start)/(end2-start2)
        if exonratio>0.6 and intronratio<0.1 and exonratio < 1.1:
            return "exon"
        elif exonratio<0.1 and intronratio>0.6:
            return "intron"
        else:
            return "exon+intron"
    else:
        return "Unknown"


Bedfile=sys.argv[1]
Dlessfile=sys.argv[2]
BED=pd.read_table(Bedfile,header=None)
DLESS=pd.read_table(Dlessfile,header=None)
BED=BED.sort_values(by=1)
BED=BED[~BED[3].str.contains("evm.model.Herato....\.[0-9]{1,3}\.[0-9]{1,2}$")]
sumtable=DLESS.iloc[:,[0,2,3,4,5,8]]
sumtable.columns=["scaf","branchtype","start","end","score","id"]
sumtable=pd.concat([sumtable, pd.DataFrame(columns=["position","reletive_gene","gene_start","gene_end","gene_strand"])])

for i in range(0,len(DLESS)):
    start=DLESS.iloc[i,3]
    end=DLESS.iloc[i,4]
    startright=0
    startleft=0
    endleft=0
    endright=0
    startleftGN=None
    startrightGN=None
    endleftGN=None
    endrightGN=None
    for j in range(0,len(BED)):
        Bedstart=BED.iloc[j,1]
        Bedend=BED.iloc[j,2]
        BedGN=BED.iloc[j,3]
        if start >= Bedstart:
            startleft=Bedstart
            startleftGN=BedGN
        elif start < Bedstart and startright==0:
            startright=Bedstart
            startrightGN=BedGN
        if end > Bedend:
            endleft=Bedend
            endleftGN=BedGN
        elif end <= Bedend and endright==0:
            endright=Bedend
            endrightGN=BedGN
        if startright!=0 and endright!=0:
            break
    if start<endright and startleftGN==endrightGN:
        CorrGene=startleftGN
        DlessType=Position_to_exon(CorrGene,start,end)
    elif startleftGN==endleftGN and start<endleft and end<startright:
        DlessType="partial_overlapped"
        CorrGene=startleftGN
    elif startleftGN==endleftGN and start>endleft and end<startright:
        DlessType="noncoding_region"
        strand1=BED[BED[3].isin([startleftGN])].iloc[0,5]
        strand2=BED[BED[3].isin([startrightGN])].iloc[0,5]
        CorrGene="NA"
        if strand1=='-' and start-endleft < 5000:
            CorrGene=startleftGN
        if strand2=='+' and startright-end < 5000:
            if CorrGene == "NA":
                CorrGene=startrightGN
            else:
                CorrGene+=","+startrightGN
    elif startleftGN==endleftGN and start<endleft and end>startright:
        DlessType="partial_overlapped"
        CorrGene=startleftGN+startrightGN
    elif startleftGN==endleftGN and start>endleft and end>startright:
        DlessType="partial_overlapped"
        CorrGene=startrightGN
    elif startrightGN==endleftGN:
        DlessType="fully_covered"
        CorrGene=startrightGN
    else:
        DlessType="Unknown"
        CorrGene="NA"
    if sumtable.loc[i,'id']==DLESS.iloc[i,8]:
        sumtable.loc[i,'position']=DlessType
        sumtable.loc[i,'reletive_gene']=CorrGene
        if CorrGene!="NA":
            if CorrGene.find(",") == -1:
                line=BED[BED[3].isin([CorrGene])]
                sumtable.loc[i,'gene_start']=line.iloc[0,1]
                sumtable.loc[i,'gene_end']=line.iloc[0,2]
                sumtable.loc[i,'gene_strand']=line.iloc[0,5]
            else:
                GN1=CorrGene[:CorrGene.find(',')]
                GN2=CorrGene[CorrGene.find(',')+1:]
                #print("CorrGene: %s\ni: %d"%(CorrGene,i))
                line1=BED[BED[3].isin([GN1])]
                line2=BED[BED[3].isin([GN2])]
                sumtable.loc[i,'gene_start']=str(line1.iloc[0,1])+","+str(line2.iloc[0,1])
                sumtable.loc[i,'gene_end']=str(line1.iloc[0,2])+","+str(line2.iloc[0,2])
                sumtable.loc[i,'gene_strand']=line1.iloc[0,5]+","+line2.iloc[0,5]  
    else:
        exit(1)
    print(DLESS.iloc[i,8])
    print("start: %s\nstartleft: %s %s\nstartright: %s %s\nend: %s\nendleft: %s %s\nendright: %s %s"%(start,startleft,startleftGN,startright,startrightGN,end,endleft,endleftGN,endright,endrightGN))
    print("%s: %s"%(DlessType,CorrGene))
    print("-----------\n")

    sumtable.to_csv("FindCorrGenes.csv",index=False,columns=["scaf","branchtype","start","end","score","id","position","reletive_gene","gene_start","gene_end","gene_strand"])



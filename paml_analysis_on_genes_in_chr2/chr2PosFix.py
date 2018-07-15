#!/usr/bin/python


import sys

mapFile=sys.argv[1] #Herato.transitions.tsv.
fstFile=sys.argv[2] #Fst bed file
outFile=sys.argv[3]

m=open(mapFile,"r")
scafLengths={}
next(data)
for line in m:
    atts=line.split()
    scafName=atts[6]
    scafLength=int(atts[8])
    scafLengths[scafName]=scafLength

f=open(fstFile,"r")
o=open(outFile,"w")
for line in f:
    atts=line.split()
    scaf=atts[0]
    start=int(atts[1])
    end=int(atts[2])+1
    name=atts[3]
    score=atts[4]
    newScaf='''%s_chr%i_%i''' % (scaf[:6],int(scaf[6:8]),16-int(scaf[8:]))
    newStart=scafLengths[newScaf]-end+1  #invert
    newEnd=scafLengths[newScaf]-start+1  #invert
    o.write('''%s\t%i\t%i\t%s\t%s\n''' % (newScaf,newStart,newEnd,name,score))


#turn their fst file to our coordinate.

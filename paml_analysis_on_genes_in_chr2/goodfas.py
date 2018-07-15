#!/usr/bin/python
import os
from Bio import AlignIO
DIR="sepgenes/realigned/"
List=os.listdir(DIR)
goodfas=[]
badfas=[]
for i in range(0,len(List)):
	print(List[i])
	
	seq_record = AlignIO.read(DIR+List[i], "fasta")
	ngap = seq_record.format("fasta").count('-')  #number of gaps
	length = seq_record.get_alignment_length()
	if ngap > 2*length:
		print("%s have too many gaps"%(List[i]))
		badfas.append([List[i],0])
		continue
	
	nATG=0     #number of atg in the first 3 position in 7 sequence (forward)
	nCAT=0     #number of cat in the last 3 position in 7 sequence (reverce)
	nsuk=0     #number of start unkown codon 
	neuk=0     #number of end unknow codon
	nsstop=0   #number of stop codon  in the first 3 position in 7 sequence (reverce)
	nestop=0   #number of stop codon in the last 3 position in 7 sequence (forward)
	direction='+'
	for seq in seq_record:
		if seq.seq.count('-')*2 > length:
			print("%s have too many gaps"%(List[i]))
			badfas.append([List[i],0])
			continue
		f3p=seq.seq[0:3].lower()
		e3p=seq.seq[-3:].lower()
		if f3p == "atg": nATG += 1
		elif f3p == "---" or f3p == "nnn": nsuk += 1
		elif f3p == "tta" or f3p == "cta" or f3p == "tca": nsstop += 1
		if e3p == "cat": nCAT += 1
		elif e3p == "---" or e3p == "nnn": neuk += 1
		elif e3p == "taa" or e3p == "tag" or e3p == "tga": nestop += 1
	if nATG/(7-nsuk) > 0.5 and nestop/(7-neuk) > 0.2: direction = '+'
	elif nCAT/(7-nsuk) > 0.5 and nsstop/(7-neuk) > 0.2: direction = '-'
	else:
		print("%s can't find ORF"%(List[i]))
		badfas.append([List[i],1])
		continue
	goodfas.append([List[i],direction])

fgood=open('goodfas.list','w')
fbad=open('badfas.list','w')
for line in goodfas:
	fgood.write(line[0]+'\t'+line[1]+'\n')
for line in badfas:
	fbad.write(line[0]+'\t'+str(line[1])+'\n')
fgood.close() 
fbad.close()
	
	


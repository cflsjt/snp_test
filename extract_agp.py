#extract physical snp location from agp file

import sys
import argparse


parser = argparse.ArgumentParser(description='AGP and SNP score combination')
parser.add_argument('-s', type=argparse.FileType('r'), help="superscaffold output file from extract_snp.py", dest='in_scaff', required=True)
parser.add_argument('-a', type=str, help="AGP file", dest='agp_file', required=True)
parser.add_argument('-c', type=argparse.FileType('r'), help="call score file", dest='call_file', required=True)
parser.add_argument('-n', type=str, help="output id for file naming", dest='call_id', required=True)
args = parser.parse_args()

A = args.agp_file
F = args.in_scaff
C = args.call_file
S = args.call_id

O = open('%s_agp_filter.out' % S, 'w')

#extract snps output file
for line in F:
    snps = line.split("\t")
    name = snps[0]
    scaff = snps[1]
    anno = snps[3].strip()
    pos = int(snps[2])
    with open('%s' % A, 'r') as T:
#agp file, with line numbers
        for line in T:
            data = line.split()
            if scaff == data[6]:
                if pos > int(data[7]) and pos < int(data[8]):
                    O.write("%s\t%s\t%s\t%s\t%d\t%s\n" % (data[0],data[1], scaff, name, pos, anno))

O.close()
O2 = open('%s_agp_scores.out' % S, 'w')

O3 = open('%s_homeless_snps.out' % S, 'w')
    
for line in C:
    calls = line.split()
    name = calls[0]
    mapped = "NO"
    if name != "Name":
        with open('%s_agp_filter.out' % S, 'r') as G:
            for entry in G:
                agps = entry.split()
                if name == agps[3]:
                    O2.write("%s\t%s" % (entry.strip(), line))
                    mapped = "YES"
    else:
        O2.write(line)
    if mapped == "NO":
        O3.write(line)
O2.close()
O3.close()
            


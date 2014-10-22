#!/usr/bin/python2.6
"""extract scores for a list of markers from fitTetra output file"""

import sys
import argparse
parser = argparse.ArgumentParser(description='GS output to fitTetra')
parser.add_argument('-m', type=argparse.FileType('r'), help="list file with marker names, required", dest='markers', required=True)
parser.add_argument('-s', type=argparse.FileType('r'), help="score output frile from fitTetra, required", dest='in_scores', required=True)
parser.add_argument('-o', type=argparse.FileType('w'), help="score output file", dest='out_file', required=True)
args = parser.parse_args()


marker_lst = []
scorefile = []
names = []
cur_marker = ""
M = args.markers
S = args.in_scores
O = args.out_file

for line in M:
    marker = line.split()
    marker_lst.append(marker[0])

for line in S:
    data = line.split("\t")
    name = data[1]
    if name in marker_lst:
        sample = data[2]
        if sample not in names:
            names.append(sample)
        score = data[13].strip()
#sometimes fitTetra doesn't output score
        if score:
            geno = score
        else:
            geno = "NS"
#deal with first marker, add samples for marker
        if cur_marker == "":
            cur_marker = name
        if cur_marker == name:
            scorefile.append(geno)
#move to next marker, output score data
        else:
            O.write("\n%s\t" % (cur_marker))
            for entry in scorefile:
                O.write("%s\t" % (entry))
            scorefile = []
            scorefile.append(geno)
            cur_marker = name
#output data for last sample
O.write("\n%s\t" % (cur_marker))
for entry in scorefile:
    O.write("%s\t" % (entry))
O.write("\nMarker\t")
for entry in names:
    O.write("%s\t" % (entry))

    


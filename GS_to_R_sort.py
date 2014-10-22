#!/usr/bin/python2.6 
"""script to manipulate Genome Studio output to fitTetra compatible
Remove first column with GS ID number before using this tool!!!! Format of marker name and sample X and Y only, remove other columns
single file output with ratio for tetraploid output.  Not dealing with diploid data."""

import sys
import argparse


parser = argparse.ArgumentParser(description='GS output to fitTetra')
parser.add_argument('-i', type=argparse.FileType('r'), help="input Genome Studio file,in format tab delimited with columns: Name(marker), sample.X(values), sample.Y(values), required", dest='in_file', required=True)
args = parser.parse_args()

tet = open("tet_ratio", 'w')
f = args.in_file
names = []
sampleID = []
data = []
samples = []
tet.write("MarkerName\tSampleName\tratio\n")
ratio_dict = {}
cur_marker = ""

for line in f:
    if line.startswith("Name"):
        #generate a list with sampleIDs
        #ignore first entry as not sampleID
        names = line.split("\t")
        names = names[1:]
        for entry in names:
            info = entry.split(".")
            sample = info[0]
            #split generates sample.x sample.y and a raw
            if sample not in samples:
                    #make a list with unique sample names
                samples.append(sample)
    else:
        data = line.split()
        marker = data[0]
        things = samples
        count_sample = len(samples)
        ratio_dict = {}
        data = data[1:]
        count_score = len(data)
        while count_sample >= 1 and count_score >= 2:
            x = float(data[0])
            y = float(data[1])
            if x == 0:
                ratio = 0
            else:
                ratio = x /(x+y)
            ratio = float(ratio)
            ID = things[0]
            ratio_dict[ID] = ratio
            data = data[2:]
            things = things[1:]
            count_sample = len(things)
            count_score = len(data)
        for key in sorted(ratio_dict.iterkeys(), key=str.lower):
            tet.write("%s\t%s\t%04f\n" % (marker, key, ratio_dict[key]))
                
tet.close()

          
                   
        

        

"""use output score file from fitTetra, lists header with 14 columns
first column marker number, second markerID, last column assigned genotype group (0, 1, 2, 3,4)
input s to be file with fitTetra score results
input t tab file with list of sampleID and type: either parent1, parent2, progeny, control(DM), diploid, sample
output file -o consist of counts for parents and progeny according to genotype group
"""

import sys
import argparse


parser = argparse.ArgumentParser(description='GS output to fitTetra')
parser.add_argument('-s', type=argparse.FileType('r'), help="score output file from fitTetra, required", dest='in_scores', required=True)
parser.add_argument('-t', type=argparse.FileType('r'), help="tab file with sampleID and type(parent1, parent2, progeny, control, diploid)", dest='sample_type', required=True)
parser.add_argument('-o', type=argparse.FileType('w'), help="output file with group counts for population and controls", dest='out_file', required=True)
parser.add_argument('-c', type=argparse.FileType('w'), help="output file with group counts for mixed samples and controls", dest='out_samples', required=True)
args = parser.parse_args()

T = args.sample_type
F = args.in_scores
o = args.out_file
t = args.out_control

def add_progeny(name):
    progeny_groups[name] += 1
        
def add_sample(name):
    if sample_groups.has_key(name):
        sample_groups[name] += 1
    else:
        sample_groups[name] = 1

def get_geno(sample, genotype):
     if sample in control_type:
         Test[sample] = genotype
     elif sample in parent_type:
         Parent[sample] = genotype
     elif sample in progeny_type:
         add_progeny(genotype)
     elif sample in sample_type:
         add_sample(genotype)
                                                                                                                                                                     
                            
progeny_groups = {"NS": 0, "0": 0, "1": 0, "2": 0, "3":0, "4": 0}
sample_groups = {}
Test = {}
Parent = {}
marker_list = []
parent_type = []
progeny_type = []
sample_type = []
control_type = []

for line in T:
    stype = line.split()
    if stype[1] == "parent1":
        parent_type.append(stype[0])
    elif stype[1] == "parent2":
        parent_type.append(stype[0])
    elif stype[1] == "progeny":
        progeny_type.append(stype[0])
    elif stype[1] == "control":
        control_type.append(stype[0])
    elif stype[1] == "sample":
        sample_type.append(stype[0])
    else:
        print("some of these entries are labelled wrongly!")
        
cur_marker = ""
for line in F:
    info = line.split("\t")
    if info[0]!= "marker":
        sampleID = info[2].strip()
        markerID = info[1].strip()
        geno = info[13].strip()
        if geno == "":
            geno = "NS"
#get the various scores from diploids and parents
#only count scores for the mapping population, exclude diploid and other samples
#check if marker in the list, if it is add to the count for the specific genotype
        if markerID in marker_list:
            if markerID == cur_marker:
                if sampleID in control_type:
                    Test[sampleID] = geno
                elif sampleID in parent_type:
                    Parent[sampleID] = geno
                elif sampleID in progeny_type:
                    add_progeny(geno)
                elif sampleID in sample_type:
                    add_sample(geno)
        else:
            if cur_marker != "":
                o.write("\n%s\t" % (cur_marker))
                t.write("\n%s\t" % (cur_marker))
                for key, value in Test.items():
                    o.write("%s:%s\t" % (key, value))
                    t.write("%s:%s\t" % (key, value))
                for key, value in Parent.items():
                    o.write("%s:%s\t" % (key, value))
                for key, value in progeny_groups.items():
                    o.write("%s:%s\t" % (key, value))
                for key, value in sample_groups.items():
                    t.write("%s:%s\t" % (key, value))
                progeny_groups = {"NS":0, "0": 0, "1": 0, "2": 0, "3": 0, "4": 0}
                sample_groups = {}
                Parents = {}
                Test = {}
                cur_marker = markerID
                marker_list.append(cur_marker)
                if sampleID in control_type:
                    Test[sampleID] = geno
                elif sampleID in parent_type:
                    Parent[sampleID] = geno
                elif sampleID in progeny_type:
                    add_progeny(geno)
                elif sampleID in sample_type:
                    add_sample(geno)
#add new markerID to the list and start counting
            else:
                cur_marker = markerID
                marker_list.append(cur_marker)
                if sampleID in control_type:
                    Test[sampleID] = geno
                elif sampleID in parent_type:
                    Parent[sampleID] = geno
                elif sampleID in progeny_type:
                    add_progeny(geno)
                elif sampleID in sample_type:
                    add_sample(geno)
if sample_groups or progeny_groups:
    o.write("\n%s\t" % (cur_marker.strip()))
    for key, value in Test.items():
        o.write("%s:%s\t" % (key, value.strip()))
    for key, value in Parent.items():
        o.write("%s:%s\t" % (key, value.strip()))
    for key, value in progeny_groups.items():
        o.write("%s:%s\t" % (key, value))
    t.write("\n%s\t" % (cur_marker.strip()))
    for key, value in Test.items():
        t.write("%s:%s\t" % (key, value))
    for key, value in sample_groups.items():
        t.write("%s:%s\t" % (key, value))
                                                                                                                                                                     
    
o.close()
t.close()

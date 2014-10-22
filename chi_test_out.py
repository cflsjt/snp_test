#take the simpXnull score file and reorganise to give numbers for use in chi test
#takes in the output file from get_null_simp.py
#retreives the parent genotypes and takes progeny counts for these genotypes
#output at tabular: marker\ genotype1 count\genotype2 count

import sys

o = open("chi_test.out", 'w')
score = []

with open(sys.argv[1],'r') as F:
    for line in F:
        counts = line.split()
        marker = counts[0]
        parent1 = counts[1].split(":")
        geno1 = parent1[1]
        parent2 = counts[2].split(":")
        geno2 = parent2[1]
        counts = counts[3:5]
        print counts
        for entry in counts:
            entry = entry.split(":")
            score.append(entry[1])
        genotype_count1 = score[0]
        genotype_count2 = score[1]
        o.write("%s\t%s\t%s\n" % (marker, genotype_count1, genotype_count2))
        score = []

o.close()

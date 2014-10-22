#to pull out those SNP markers that are nulliplex x simplex for initial mapping
#create 2 files, where control DM is expected group of 0 or 4, second group where
#DM not as expected but progeny scores are same as parents as derived from null x simp
#takes 2 files, first is group conts from fittetra_group_counts, second is sample type file to distinguish parent and controls
#here control is DM which is homozygous diploid

import sys

good_con = ["0", "4"]
genotypes = ["NS", "0", "1", "2","3", "4"]
Progeny = []
Parent1 = []
Parent2 = []
parent1score = []
parent2score = []
controlscore = []
Controls = []
score = []
samples = {}

o = open("null_simplex_list", 'w')


with open(sys.argv[2], 'r') as T:
    for entry in T:
        types = entry.split()
        type = types[1].strip()
        if types[1] == "parent1":
#            print types[0]
            Parent1.append(types[0])
        elif types[1] == "parent2":
            Parent2.append(types[0])
        elif types[1] == "control":
            Controls.append(types[0])
            
with open(sys.argv[1], 'r') as F:
    for line in F:
        line = line.strip()
        scores = line.split("\t")
#        print scores
        marker = scores[0]
        scores = scores[1:]
        number = 0
        missing = "0"
        dubred = "0"
        for group in scores:
            grp = group.split(":")
#            print grp
            geno = grp[0]
            value = grp[1]
            #get parent genotypes
            if geno in Parent1:
                if value not in parent1score:
                    if value != "NS":
                        parent1score.append(value)
            elif geno in Parent2:
                if value not in parent2score:
                    if value != "NS":
                        parent2score.append(value)
            elif geno in Controls:
                if value not in controlscore:
                    if value != "NS":
                        controlscore.append(value)
            elif geno in genotypes:
                if geno == "NS":
                    missing = int(value)
                else:
                    if value != "0":
                        samples[geno] = value
                number += int(value)
        print number        
        #check ratio of no scores (NS)
        #check for double reduction
        for key, value in samples.iteritems():
            if key != "NS":
                if int(value) >= number*0.05:
                    Progeny.append(key)
                    score.append(value)
                else:
                    dubred = value
        if missing  <= number*0.10:
#            print missing
            #compare parent scores and progeny scores
            #check parent duplicates
            if len(parent1score) == 1:
                parent1 = parent1score[0]
                if len(parent2score) == 1:
                    parent2 = parent2score[0]
#                    print parent2score
                    parents = set(parent1score + parent2score)
#                    print parents
                    Progeny = set(Progeny)
                    if len(Progeny) == 2:
                        progeny1 = score[0]
                        progeny2 = score[1]
#                    print Progeny
                        if len(controlscore) == 1:
                        #get "good set"
                            score = controlscore[0]
                            if score in good_con:
                                if Progeny == parents:
                                    grade = "high"
                            elif Progeny == parents:
                                    grade = "medium"
                            else:
                                grade = "low"
                            o.write("%s\tparent1:%s\tparent2:%s\tprogeny1:%s\tprogeny2:%s\tdred:%s\t%s\n" % (marker, parent1, parent2, progeny1, progeny2, dubred, grade))
                                    
        score = []                
        parent1score = []
        parent2score = []
        Progeny = []
        controlscore = []
        samples = {}
            
o.close()
            
            
        

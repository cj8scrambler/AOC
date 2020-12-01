#!/usr/bin/python

import sys
import fileinput
import difflib

done = False
doubles = 0
triples = 0
count = dict()

with open(sys.argv[1], 'r') as source_f:
    for source in source_f:
        with open(sys.argv[1], 'r') as target_f:
            for target in target_f:
                #print("%s : %s" % (source, target))
                diffs = 0
                common = ""
                for i,s in enumerate(difflib.ndiff(source, target)):
                    if s[0]=='-':
                        diffs += 1
                    elif s[0]==' ':
                        common += s[2]
                #print("  Total %d diffs" % (diffs))
                if (diffs == 1):
                    print("%s : %s" % (source, target))
                    print("  Total %d diffs" % (diffs))
                    print("  THIS IS IT: %s", common)

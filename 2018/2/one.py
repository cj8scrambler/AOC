#!/usr/bin/python

import sys
import fileinput

done = False
doubles = 0
triples = 0
count = dict()

with open(sys.argv[1], 'r') as data:
    for line in data:
        print("LINE: %s" % (line))
        count.clear()
        for c in line:
            count[c] = count.get(c, 0) + 1
        if (2 in count.values()):
            print("  has a double")
            doubles += 1
        if (3 in count.values()):
            print("  has a tripple")
            triples += 1
    print ("Checksum: %d" % (doubles * triples))

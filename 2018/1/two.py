#!/usr/bin/python

import sys
import fileinput

done = False
freq = 0
i = 0
counts = dict()

while not done:
    with open(sys.argv[1], 'r') as data:
        for line in data:
            freq = eval(str(freq) + line)
            i += 1
            counts[freq] = counts.get(freq, 0) + 1
            if (counts[freq] == 2):
                print ("i: %d freq: %d  count: %d" % (i, freq, counts[freq]))
                done = True

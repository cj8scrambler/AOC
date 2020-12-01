#!/usr/bin/python

import sys
import fileinput
import difflib

dups = 0
count = dict()

with open(sys.argv[1], 'r') as source_f:
    for source in source_f:
        origin = source.split()[2][:-1]
        size = source.split()[3]
        print("origin: %s   size: %s" % (origin, size))
        ox = int(origin.split(',')[0])
        oy = int(origin.split(',')[1])
        sx = int(size.split('x')[0])
        sy = int(size.split('x')[1])
        print("  (%d,%d) : (%d,%d)" % (ox,oy,sx,sy))
        while (sx):
            sy = int(size.split('x')[1])
            while (sy):
                x = ox + sx 
                y = oy + sy 
                print("    %d,%d" % ((ox+sx-1), (oy+sy-1)))
                count.setdefault(x,{})[y] = count.setdefault(x,{}).setdefault(y,0) + 1
                sy -= 1
            sx -= 1

    print(count)

    for x in count:
        for y in count[x]:
            if (count[x][y] >= 2):
                dups += 1
                print("  (%d,%d) : %d" % (x, y, count[x][y]))
    print("Total overlaps: %d" % dups)

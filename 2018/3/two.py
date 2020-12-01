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
#        print("origin: %s   size: %s" % (origin, size))
        ox = int(origin.split(',')[0])
        oy = int(origin.split(',')[1])
        sx = int(size.split('x')[0])
        sy = int(size.split('x')[1])
#        print("  (%d,%d) : (%d,%d)" % (ox,oy,sx,sy))
        while (sx):
            sy = int(size.split('x')[1])
            while (sy):
                x = ox + sx 
                y = oy + sy 
#                print("    %d,%d" % ((ox+sx-1), (oy+sy-1)))
                count.setdefault(x,{})[y] = count.setdefault(x,{}).setdefault(y,0) + 1
                sy -= 1
            sx -= 1

    for x in count:
        for y in count[x]:
            if (count[x][y] >= 2):
                dups += 1
#                print("  (%d,%d) : %d" % (x, y, count[x][y]))

    with open(sys.argv[1], 'r') as source_c:
        for check in source_c:
            valid = 1
            line = check.split()[0]
            origin = check.split()[2][:-1]
            size = check.split()[3]
            ox = int(origin.split(',')[0])
            oy = int(origin.split(',')[1])
            sx = int(size.split('x')[0])
            sy = int(size.split('x')[1])
#            print("  %s (%d,%d) : (%d,%d)" % (line, ox,oy,sx,sy))
            while (sx):
                sy = int(size.split('x')[1])
                while (sy):
                    x = ox + sx 
                    y = oy + sy 
                    if (count[x][y] != 1):
#                        print("    %d,%d is invalid" % (x,y))
                        valid = 0
#                    count.setdefault(x,{})[y] = count.setdefault(x,{}).setdefault(y,0) + 1
                    sy -= 1
                sx -= 1
            if (valid):
                print("%s (%d,%d) : (%d,%d) is valid" % (line,ox,oy,sx,sy))

    print("Total overlaps: %d" % dups)

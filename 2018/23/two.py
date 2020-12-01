#!/usr/bin/python3

import sys
import copy
import re
import operator

nano = []
max_x = 0
max_y = 0
max_z = 0
#srange = [set(),set(),set()] # source range x/y/z
srange = [[],[],[]]

max_in_range = 0
in_range = []

def list_between(val1, val2):
    if (val1 > val2):
        return(list(range(val2, val1)))
    return(list(range(val1, val2)))

def uniques(seq):
   # Not order preserving
   keys = {}
   for e in seq:
       keys[e] = 1
   return list(keys.keys())

def distance(obj1, obj2):
    distance = (abs(obj1[0]-obj2[0]) + abs(obj1[1]-obj2[1]) +abs(obj1[2]-obj2[2]))
#    print("  distance from (%d,%d,%d)[%d] -> (%d,%d,%d)[%d]: %d" % (obj1[0], obj1[1], obj1[2], obj1[3], obj2[0], obj2[1], obj2[2], obj2[3], distance))
    return distance

with open(sys.argv[1], 'r') as source_f:
    max_radius = 0
    for source in source_f:
        g = re.match( r"pos=<(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)>, r=([0-9]+)", source)
        if g:
            x = int(g.group(1))
            y = int(g.group(2))
            z = int(g.group(3))
            r = int(g.group(4))
            nano.append([x,y,z,r])
            if (r > nano[max_radius][3]):
                max_radius = len(nano)-1
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            if z > max_z:
                max_z = z
            print("x range %d - %d" % (x-r, x+r+1))
            #for i in range(x-r, x+r+1):
            #    srange[0].add(i);
            srange[0] = srange[0] + list_between(x-r, x+r+1)
            #for i in range(y-r, y+r+1):
            #    srange[1].add(i);
            print("y range %d - %d" % (y-r, y+r+1))
            srange[1] = srange[0] + list_between(y-r, y+r+1)
            #for i in range(z-r, z+r+1):
            #    srange[2].add(i);
            print("z range %d - %d" % (z-r, z+r+1))
            srange[2] = srange[0] + list_between(z-r, z+r+1)
            print("Added (%d,%d,%d)[%d]  maxes: %d/%d/%d" % (x,y,z,r, max_x, max_y, max_z))
            print("x range: %s" % (srange[0]))
        else:
            print("Invalid data: %s" % (source))
            exit

print("srange x has %d elements: %s" % (len(srange[0]), srange[0]))
srange[0] = uniques(srange[0])
print("unique srange x has %d elements: %s" % (len(srange[0]), srange[0]))

print ("Max: [%d, %d, %d] max radius element-#%d: %d" % (max_x, max_y, max_z, max_radius, nano[max_radius][3]))
sum = 0
for each in nano:
    if (distance(nano[max_radius], each) <= nano[max_radius][3]):
        sum += 1
print ("Answer #1: %d nanbots in range" % sum)

count=0
for x in range(max_x):
    for y in range(max_y):
        for z in range(max_z):
            count += 1
#            if ((count % 100000) == 0):
            if ((count % 1000) == 0):
                print("count=%d [%d, %d, %d] (%.1f %% done)" % (count, x, y, z, float(x / max_x) * 100.0))
            if ((x in srange[0]) and (y in srange[1]) and (z in srange[2])):
                total = 0
                for each in nano:
                    if (distance([x,y,z,99999,0], each) <= each[3]):
                        total += 1
#                print("[%d,%d,%d] has %d in range" % (x, y, z, total))
                if (total > max_in_range):
                    max_in_range = total
                    del in_range[:]
                    in_range.append([x,y,z,9999,0])
                    print("Reset best to value %d" % (max_in_range))
                elif (total == max_in_range):
                    in_range.append([x,y,z,9999,0])
#                    print("Added to best value %d : %s" % (max_in_range, in_range))
    
print("Points which are %d away: %s" % (max_in_range, in_range))

#!/usr/bin/python3

import sys
import copy
import re
import operator

nano = []
max_x = 0
max_y = 0
max_z = 0
max_in_range = 0
in_range = []

def distance(obj1, obj2):
    distance = (abs(obj1[0]-obj2[0]) + abs(obj1[1]-obj2[1]) +abs(obj1[2]-obj2[2]))
#    print("  distance from (%d,%d,%d)[%d] -> (%d,%d,%d)[%d]: %d" % (obj1[0], obj1[1], obj1[2], obj1[3], obj2[0], obj2[1], obj2[2], obj2[3], distance))
    return distance

with open(sys.argv[1], 'r') as source_f:
    max_radius = 0
    for source in source_f:
        g = re.match( r"pos=<(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)>, r=([0-9]+)", source)
        if g:
            nano.append([int(g.group(1)),int(g.group(2)),int(g.group(3)),int(g.group(4)), 0])
            if (nano[len(nano)-1][3] > nano[max_radius][3]):
                max_radius = len(nano)-1
            if nano[len(nano)-1][0] > max_x:
                max_x = nano[len(nano)-1][0]
            if nano[len(nano)-1][1] > max_y:
                max_y = nano[len(nano)-1][1]
            if nano[len(nano)-1][2] > max_z:
                max_z = nano[len(nano)-1][2]
            print("Added (%d,%d,%d)  maxes: %d/%d/%d" % (nano[len(nano)-1][0], nano[len(nano)-1][1], nano[len(nano)-1][2], max_x, max_y, max_z))
        else:
            print("Invalid data: %s" % (source))
            exit

print ("Max: [%d, %d, %d] max radius element-#%d: %d" % (max_x, max_y, max_z, max_radius, nano[max_radius][3]))
sum = 0
for each in nano:
    if (distance(nano[max_radius], each) <= nano[max_radius][3]):
        sum += 1
print ("Answer #1: %d nanbots in range" % sum)

for x in range(max_x):
    for y in range(max_y):
        for z in range(max_z):
            if ((z % 1000000) == 0):
                print("[%d, %d, %d] (%.1f %% done)" % (x, y, z, float(x / max_x) * 100.0))
            total = 0
            for each in nano:
                if (distance([x,y,z,99999,0], each) <= each[3]):
                    total += 1
#            print("[%d,%d,%d] has %d in range" % (x, y, z, total))
            if (total > max_in_range):
                max_in_range = total
                del in_range[:]
                in_range.append([x,y,z,9999,0])
                print("Reset best to value %d" % (max_in_range))
            elif (total == max_in_range):
                in_range.append([x,y,z,9999,0])
#                print("Added to best value %d : %s" % (max_in_range, in_range))

print("Points which are %d away: %s" % (max_in_range, in_range))

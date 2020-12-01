#!/usr/bin/python3

import sys
import copy
import re
import operator

stars = []

def convert(whatitwas, whatitwillbe):
#    print("      Convert all instances of const-%d to const-%d" % (whatitwas, whatitwillbe))
    for star in stars:
        if (star[4] is whatitwas):
            star[4] = whatitwillbe

def distance(obj1, obj2):
    distance = (abs(obj1[0]-obj2[0]) + abs(obj1[1]-obj2[1]) +
                abs(obj1[2]-obj2[2]) + abs(obj1[3]-obj2[3]))
    return distance

with open(sys.argv[1], 'r') as source_f:
    for source in source_f:
        stars.append([int(x) for x in source.split(",")] + [0])
#        print("Added: %s" % (stars[len(stars)-1]))

new_const = 1
stars[0][4] = new_const
new_const += 1
for frog in range(len(stars)):
    from_const = stars[frog][4]
#    print ("From: %s" % (stars[frog]))
    to = frog+1
    if (to < len(stars)):
        for to in range(to, len(stars)):
#            print ("    to: %s" % (stars[to]))
            if (stars[frog][4] != stars[to][4]):
                if (distance(stars[frog], stars[to]) <= 3):
                    if (stars[to][4] is 0):
                        stars[to][4] = from_const
#                        print("      close; add to const-%d" % (from_const))
                    else:
                        convert(stars[to][4], from_const)
                else:
                    if (stars[to][4] is 0):
#                        print("      far; new const-%d" % (new_const))
                        stars[to][4] = new_const
                        new_const += 1
#            else:
#                print("      skip; already in const-%d" % (stars[to][4]))


print("Final Map:")
num_const = set()
for star in stars:
    print("%d: [%d,%d,%d,%d]" % (star[4], star[0], star[1], star[2], star[3]))
    num_const.add(star[4])
print("Total Constallations: %d" % (len(num_const)))

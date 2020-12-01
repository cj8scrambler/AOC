#!/usr/bin/python3

import sys
import copy
import re
import operator

map = []

def count_type(type):
    sum = 0
    for y in range(len(map)):
        for x in range(len(map[y])):
            if (map[y][x] is type):
                sum += 1
    return sum

def print_map():
    for y in range(len(map)):
        for x in range(len(map[y])):
            print("%c" % (map[y][x]), end="")
        print("")

def adjacent(loc_x, loc_y, type):
#    print("Count '%c' neighbors of [%d,%d]" % (type, loc_x, loc_y));
    sum = 0
    for y in range(loc_y - 1, loc_y + 2): 
        if ((y >= 0) and (y < len(map))):
            for x in range(loc_x - 1, loc_x + 2): 
                if ((x >= 0) and
                    (x < len(map[y])) and
                    (not ((x is loc_x) and (y is loc_y)))):
                    if (map[y][x] is type):
#                        print("  [%d,%d] neighbor [%d,%d] matches '%c'" % (loc_x, loc_y, x, y, type));
                        sum += 1
    return sum
    

def tick():
    global map

    source = copy.deepcopy(map)
    for y in range(len(source)):
        for x in range(len(source[y])):
            if (source[y][x] is '.'):
                if (adjacent(x, y, '|') >= 3):
#                    print("Update %d,%d to tree" % (x,y))
                    source[y][x] = '|'
            elif (source[y][x] is '|'):
                if (adjacent(x, y, '#') >= 3):
#                    print("Update %d,%d to lumberyard" % (x,y))
                    source[y][x] = '#'
            elif (source[y][x] is '#'):
#                print("On lumberyard (%d,%d).  %d neigbor lumberyards;  %d neighbor trees" % (x, y, adjacent(x, y, '#'), adjacent(x, y, '|')))
                if (not (adjacent(x, y, '#') >= 1)) or (not (adjacent(x, y, '|') >= 1)):
#                    print("Update %d,%d to open" % (x,y))
                    source[y][x] = '.'
    map = source

with open(sys.argv[1], 'r') as source_f:
    for source in source_f:
        map.append(list(source.rstrip()))

    print ("Initial")
    print_map()
    print ("")

#    for step in range(10):
    for step in range(1000000000):
#        print ("Step #%d" % (step+1))
        tick()
#        print_map()

        w = count_type('|')
        l = count_type('#')
#        print("After %d minutes: %d Wooded Acres;  %d lumberyards; product = %d" % (step, w, l, w * l))
        if ((step % 1000) == 0):
            print("%d,%d" % (step, w * l))
#        print ("")

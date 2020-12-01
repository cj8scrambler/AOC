#!/usr/bin/python3

import sys
import re
import operator

map = []

def print_map():
    for y in range(len(map)):
        for x in range (len(map[y])):
            print("%c" % (map[y][x]), end="")
            x +=1
        print("");
        y +=1

def chosen(x,y):
    global map

    print ("Working on [%d, %d]" % (x,y))

    range = in_range(x,y)
    for (each) in range[:]:
        print ("  [%d,%d] is in range of [%d,%d]" % (each[0], each[1], x, y))
        if not reachable(each):
            print ("  [%d, %d] is not reachable" % (each[0], each[1]))
            range.remove(each)

    for near_y in range(len(map)):
        for near_x in range(len(map[y])):
            if (near_x, near_y) in range:
                print ("  [%d, %d] the chosen nearest reachable point" % (near_x, near_y))
                return (near_x, near_y)

    raise Exception("Could not find valid target from [%d,%d]" % (x,y))

def find_step(from, to):
    ''' Returns the next step as (x,y) that from should make ```
    global map

    min=10000000
    distance = [] * len(map)

    for y in range(len(map)):
        distance = [1000000] * len(map[y])
        for x in range(len(map[y])):
            if map[y][x] is '.':
                distance[y][x] = abs(from[0] - to[0]) + abs(from[1] - to[1])
                if distance[y][x] < min:
                    min = distance[y][x]

    for y in range(len(map)):
        for x in range(len(map[y])):
            if distance[y][x] is min:
                return(x,y)
    
with open(sys.argv[1], 'r') as source_f:
    y=0
    for source in source_f:
        map.append(list(source.rstrip()))
        y += 1
                
    print_map()

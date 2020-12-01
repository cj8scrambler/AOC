#!/usr/bin/python3

import sys
import re
import operator
import csv

map = {}
collisions = []
x = 0
y = 0
len = 0

def print_map():
    y = 0
    while y < len(map):
        x = 0
        while x < len(map[y]):
            print("%c" % (map[y][x]), end="")
            x +=1
        print("");
        y +=1

def move(dx, dy):
    global map
    global collisions
    global x
    global y
    global len
    global wirenum

    len -= 1  # First move doesn't count so pre-decrement
    if (dx != 0):
        xdir = int(dx / abs(dx))
        for x in range(x, x+dx+xdir, xdir):
            len += 1
            key = str(x)+","+str(y)
            if (key in map) and (map[key][0][0] != wirenum):
                if (key != '0,0'):
                    print("    %d,%d: Collision with %s; len = %d + %d" % (x,y,map[key], map[key][0][1], len))
                    collisions.append([key, map[key][0][1] + len])
            else:
                #print("    %d,%d: wire-%d len-%d" % (x,y,wirenum,len))
                map.setdefault(key, []).append([wirenum,len])

    if (dy != 0):
        ydir = int(dy / abs(dy))
        for y in range(y, y+dy+ydir, ydir):
            len += 1
            key = str(x)+","+str(y)
            if (key in map) and (map[key][0][0] != wirenum):
                if (key != '0,0'):
                    print("    %d,%d: Collision with %s; len = %d + %d" % (x,y,map[key], map[key][0][1], len))
                    collisions.append([key, map[key][0][1] + len])
            else:
                #print("    %d,%d: wire-%d len-%d" % (x,y,wirenum,len))
                map.setdefault(key,[]).append([wirenum,len])

def manh_d(x1, y1, x2=0, y2=0):
    return (abs(x1-x2) + abs(y1-y2))

wirenum=0
with open(sys.argv[1], 'r') as csvfile:
    for wire in csv.reader(csvfile, delimiter=','):
        x = 0
        y = 0
        len = 0
        wirenum += 1
        print ("Wire %d" % (wirenum))
        for step in wire:
            dir = step[0]
            num = int(step[1:])
            if (dir == 'U'):
                move(0,num);
            elif (dir == 'D'):
                move(0,-num);
            elif (dir == 'R'):
                move(num,0);
            elif (dir == 'L'):
                move(-num,0);
            print ("  %s: %s  %d  =>  %d,%d" % (step, dir, num, x, y))

min_d = 100000000000000000000
min_c = ''
for col in collisions:
    print("Collision entry: %s" % col)
    cx = int(col[0].split(',')[0])
    cy = int(col[0].split(',')[1])
    d = col[1]
    if (d < min_d):
        min_d = d;
        min_c = col;
print ("\nMinimum: %s (%d)" % (min_c, min_d))

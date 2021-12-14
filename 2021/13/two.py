#!/usr/bin/python3

import logging
import sys
import fileinput
import csv
import time
import re
import statistics
import copy
from collections import deque
from functools import reduce

def pdata(points, size_y, size_x):

    dots=0
    s = ""
    for y in range(size_y+1):
        for x in range(size_x+1):
            if (x,y) in points:
                s += "#"
                dots += 1
            else:
                s += "."
        s += "\n"
    print("Total: {}".format(dots))
    return s

def part1(points, ymax, xmax):

    for count,ins in enumerate(instructions):
        (dir, val) = ins.split()[-1].split('=')
        val = int(val)
        for i,p in enumerate(points):
            if dir == 'y':
                points[i] = (p[0], min(p[1], 2*val-p[1]))
                logging.debug(" flip {} on y={} flipped; {}".format(p, val, points[i]))
            if dir == 'x':
                points[i] = (min(p[0], 2*val-p[0]), p[1])
                logging.debug(" flip {} on x={} flipped; {}".format(p, val, points[i]))

        if dir == 'y':
            logging.debug("Update ymax from {} to {}".format(ymax, int((ymax-1)/2)))
            ymax = int((ymax-1)/2)
        if dir == 'x':
            logging.debug("Update ymax from {} to {}".format(xmax, int((xmax-1)/2)))
            xmax = int((xmax-1)/2)

        logging.info("after instruction: {}  dir={}  val={}  size={}".format(ins, dir, val, len(set(points))))
#        logging.info("\n" + pdata(points, ymax, xmax))

    logging.info("\nFinal map:\n" + pdata(points, ymax, xmax))

    return 0

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    ymax = xmax = 0
    points = []
    instructions = []
    for line in fileinput.input():
        #data.append([(int(i[0]), int(i[1])) for i in line.rstrip().split(',')])
        if line.rstrip() == "":
            continue

        try:
            points.append(tuple(map(int, line.rstrip().split(','))))
            if int(points[-1][0]) > xmax:
                xmax = int(points[-1][0])
            if int(points[-1][1]) > ymax:
                ymax = int(points[-1][1])
        except:
            #instructions.append(points.pop()[0].split()[-1])
            instructions.append(line.rstrip())

    logging.debug('size: {} x {}'.format(xmax+1,ymax+1))
    logging.debug('points {}'.format(points))
    logging.debug('instructions {}'.format(instructions))
    logging.info("initial points size={}".format(len(set(points))))
    logging.debug('initiial paper:')

    before = time.time()
    result = part1(points,ymax,xmax)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

#!/usr/bin/python3

import logging
import sys
import fileinput
import csv
import time
import re
import statistics
import copy
import math
import heapq
from collections import deque
from collections import Counter
from functools import reduce

def psource(newmap):
    out='\n'
    for y in range(len(newmap)):
        for x in range(len(newmap[0])):
            out += "{:1d}".format(newmap[y][x])
        out += '\n'
    return out

def psolved(data, h, w):
    out='\n'
    for y in range(h):
        for x in range(w):
            if (y,x) in data:
                out += "{:3d}".format(data[(y,x)])
            else:
                out += ' # '
        out += '\n'
    return out

def dijkstra(data):

    solved = {}
    current_best = []
    heapq.heappush(current_best, (0, (0,0)))
    size_y = len(data)
    size_x = len(data[0])

    # Run till we solve the end point
    while ( (size_y-1, size_x-1) not in solved.keys()):

        (cost, (y,x)) = heapq.heappop(current_best)
        if (y,x) in solved.keys():
            continue

        logging.debug("Solving for {}".format((y,x)))
        solved[(y,x)] = cost

        for ny,nx in [(y, x+1), (y+1, x), (y-1, x), (y, x-1)]:
            if (ny < 0) or (ny >= len(data)) or \
               (nx < 0) or (nx >= len(data[0])) or \
               (ny, nx) in solved:
                continue


            # Push neighbor cost to heapq.  It might be a duplicate
            # but heapq will assure that the lower cost value is
            # returned first.
            ncost = cost + data[ny][nx]
            heapq.heappush(current_best, (ncost, (ny,nx)))
            logging.debug("  add cost:({},{})".format(ncost, (ny,nx)))

    logging.info(psolved(solved, size_y, size_x))

    return solved[(size_y-1,size_x-1)]

def part1(data):
    return dijkstra(data)

def part2(data):

    newmap = []

    height = len(data)
    width = len(data[0])
    
    for oy in range(5):
        for y in range(height):
            line= []

            if oy == 0:
                source = data[y]
            else:
                source = newmap[height*(oy-1)+y]
            for ox in range(5):
                for x in range(width):
                    if ox > 0:
                        n = line[x+(ox-1)*width] + 1
                    else:
                        n = source[x]
                        if oy > 0:
                            n += 1
                    if n > 9:
                        n = 1
                    line.append(n)
            newmap.append(line)
    logging.debug("Expanded map:")
    logging.debug(psource(newmap))

    return dijkstra(newmap)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    data = []
    for line in fileinput.input():
        data.append([int(i) for i in line.rstrip()])

    logging.debug('data: {}'.format(data))

    before = time.time()
    result = part1(data)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(data)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

#!/usr/bin/python3

import logging
import sys
import fileinput
import csv
import time
import re
import statistics
import copy
from functools import reduce

# If any neighbor (N/S/E/W) is lower, return false; otherwise return true
def is_lowest(y, x, data):
    for ny,nx in [(y,x-1), (y, x+1), (y-1, x), (y+1, x)]:
        if (ny >= 0) and (ny < len(data)) and (nx >= 0) and (nx < len(data[y])):
            if (data[y][x] >= data[ny][nx]):
                return False

    logging.debug("  data[{}][{}] is a low point; return true".format(y, x)) 
    return True


def part1(data):

    risk = 0
    for iy, y in enumerate(data):
        for ix, x in enumerate(y):
            if is_lowest(iy, ix, data):
                risk += data[iy][ix] + 1
                logging.debug("[{}][{}] ({} is a low point; risk: {}".format(iy, ix, data[iy][ix], risk))

    return risk

def basin_r(bmap, data, y, x):

    if (y < 0) or (y >= len(data)) or    \
       (x < 0) or (x >= len(data[y])) or \
       (data[y][x] == 9) or bmap[y][x]:
        return 0

    logging.debug("  [{}][{}] is in basin".format(y,x))
    bmap[y][x] = 1

    # check above
    basin_r(bmap, data, y-1, x)

    # check left
    basin_r(bmap, data, y, x-1)

    # check right
    basin_r(bmap, data, y, x+1)

    # check below
    basin_r(bmap, data, y+1, x)

    logging.debug("  [{}][{}]  bmap: {}".format(y,x, bmap))

# Make a map of the basin starting at (y,x)
def basin_size(data, y, x):

    size = 0
    bmap = [ [0] * len(data[0]) for i in range(len(data))]

    logging.debug("bmap: {}".format(bmap))

    # Recursively check neighbors
    basin_r(bmap, data, y, x)

    for y in bmap:
        size += sum(y)
    logging.debug("bmap value: {}".format(size))
    
    return size


def part2(data):

    basins = []
    for iy, y in enumerate(data):
        for ix, x in enumerate(y):
            if is_lowest(iy, ix, data):
                basins.append(basin_size(data, iy, ix))
                logging.debug("[{}][{}] basin size: {}".format(iy, ix, basins[-1]))

    
    logging.debug("basin sizes: {}".format(basins))
    basins.sort(reverse=True)
    logging.debug("basin sizes sorted:: {}".format(basins))
    return (basins[0] * basins[1] * basins[2])

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    data = []
    inp = fileinput.input()
    for line in fileinput.input():
        data.append([int(i) for i in line.rstrip()])

    logging.debug('Initial data: {})'.format(data))

    before = time.time()
    result = part1(data)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(data)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

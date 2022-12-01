#!/usr/bin/python3

import logging
import sys
import fileinput
import csv
import time
import re
import copy
from functools import reduce

def pdata(data):

    out = '\n'
    for y,row in enumerate(data):
        for x,val in enumerate(row):
            out += val
        out += '\n'
    return out

def part1(data):


    moves = 1
    steps = 0
    h = len(data)
    w = len(data[0])

    logging.info("Initial map: {}".format(pdata(data)))

    while moves > 0:
        moves = 0
        steps += 1

        newdata = [['.'] * w for y in range(h)]
        logging.debug(newdata)

        # Rights
        for y,row in enumerate(data):
            for x,val in enumerate(row):
                logging.debug("{}: {} right: {}".format((y,x), data[y][x], data[y][(x+1)%w]))
                if val == '>':
                    if data[y][(x+1)%w] == '.':
                        newdata[y][(x+1)%w] = '>'
                        moves += 1
                    else:
                        newdata[y][x] = '>'

        # Downs
        for y,row in enumerate(data):
            for x,val in enumerate(row):
                logging.debug("{}: {} down: {}".format((y,x), data[y][x], newdata[(y+1)%h][x]))
                if val == 'v':
                    # check for 'v' in orig map and '>' in new map
                    if data[(y+1)%h][x] != 'v' and newdata[(y+1)%h][x] != '>':
                        newdata[(y+1)%h][x] = 'v'
                        moves += 1
                    else:
                        newdata[y][x] = 'v'

        logging.info("After {} moves on step {}: {}".format(moves, steps, pdata(newdata)))
        data = copy.deepcopy(newdata)

    return steps

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    data = []
    with open(sys.argv[1]) as inp:
        for line in inp:
            data.append([ c for c in line.rstrip()])

    before = time.time()
    result = part1(data)
    after = time.time()
    print("part 1 result: {}".format(result))

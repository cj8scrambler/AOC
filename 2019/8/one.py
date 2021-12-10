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

def part1(data, w, h):

    i = 0
    layer = 0
    img   = []
    counts   = []
    while (i < len(data)):
        img.append([])
        counts.append([ 0 for c in range(10) ])
        for y in range(0, h):
            img[layer].append([])
            for x in range(0, w):
                img[layer][y].append(data[i])
                counts[layer][data[i]] += 1
                i += 1
        layer += 1
    logging.debug("Image is:")
    for i,l in enumerate(img):
        logging.debug("layer-{}".format(i))
        for y in l:
            logging.debug("  {}".format(y))

    min_zeros = 9999999
    product = 0
    for l,c in enumerate(counts):
        if c[0] < min_zeros:
            min_zeros = c[0]
            product = c[1] * c[2]
            logging.debug("new best found on layer-{}: {}  (product: {})".format(l, c[0], product))

    return product

def part2(data, w, h):

    i = 0
    layer = 0
    img   = []
    while (i < len(data)):
        img.append([])
        for y in range(0, h):
            img[layer].append([])
            for x in range(0, w):
                img[layer][y].append(data[i])
                i += 1
        layer += 1
    logging.debug("Image is:")
    for i,l in enumerate(img):
        logging.debug("layer-{}".format(i))
        for y in l:
            logging.debug("  {}".format(y))

    final = [ [ None ] * w for i in range(h) ]
    for i,l in enumerate(img):
        for y,row in enumerate(l):
            for x,val in enumerate(row):
                if (final[y][x] is None) and (val != 2):
                    final[y][x] = val
                    logging.debug("layer-{} y-{} x-{}: {}".format(i, y, x, val))
    print("Image is:")
    for y in final:
        for x in y:
            if x:
                print('#', end='')
            else:
                print(' ', end='')
        print('')

    return 0

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    data = []
    for line in fileinput.input():
        logging.debug("line: {}".format(line))
        data = ([int(i) for i in line.rstrip()])

    logging.debug('Initial data: {})'.format(data))

    before = time.time()
    #result = part1(data, 3, 2)
    result = part1(data, 25, 6)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    #result = part2(data, 2, 2)
    result = part2(data, 25, 6)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

#!/usr/bin/python3

import logging
import sys
import fileinput
import csv
import time
import re
from functools import reduce

def intify(data):
    for d in data:
        for (k,e) in d.items():
            try:
                d[k] = int(e)
            except:
                continue

def maplines(data, do_diags=False):
    xmax = max([ x['x1'] for x in data ] + [ x['x2'] for x in data ]) + 1
    ymax = max([ y['y1'] for y in data ] + [ y['y2'] for y in data ]) + 1
    rmap = [[0] * xmax for i in range(ymax)]

    logging.debug("Create {}x{} map: {}".format(ymax, xmax, rmap))

    for p in data:
        logging.info("point: ({},{}) -> ({},{})".format(p['x1'],p['y1'],p['x2'],p['y2']))

        if (not do_diags):
            if ((p['x1'] != p['x2']) and (p['y1'] != p['y2'])):
                logging.info("  skipping diagonal");
                continue

        steps = max(abs(p['y1']-p['y2']), abs(p['x1']-p['x2']))
        if(p['y1'] > p['y2']):
            yrange = range(p['y1'], p['y2']-1, -1)
        else:
            if(p['y1'] < p['y2']):
                yrange = range(p['y1'], p['y2']+1, 1)
            else:
                yrange = [p['y1'] for y in range(steps+1)]
        logging.debug("  yrange: {}".format(yrange))

        if(p['x1'] > p['x2']):
            xrange = range(p['x1'], p['x2']-1, -1)
        else:
            if(p['x1'] < p['x2']):
                xrange = range(p['x1'], p['x2']+1, 1)
            else:
                xrange = [p['x1'] for x in range(steps+1)]
        logging.debug("  xrange: {}".format(xrange))

        for i in range(steps+1):
            rmap[yrange[i]][xrange[i]] += 1
        #print("rmap:")
        #for y in rmap:
        #    for x in y:
        #      print("{:1}".format(x), end='')
        #    print("")

    count_2plus = 0
    for y in range(ymax):
        for x in range(xmax):
            if rmap[y][x] >= 2:
                logging.debug("y={}  x-{}: {}".format(y, x, rmap[y][x]))
                count_2plus += 1
    return count_2plus

if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)

    pattern = re.compile(r"(?P<x1>\d+),(?P<y1>\d+) -> (?P<x2>\d+),(?P<y2>\d+)")
    data = [pattern.match(line).groupdict() for line in fileinput.input()]

    if (len(data) == 0):
        print("Unable to read any data")
        sys.exit(1)

    #convert the strings to ints
    intify(data)

    before = time.time()
    result = maplines(data)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = maplines(data, True)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

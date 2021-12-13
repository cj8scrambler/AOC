#!/usr/bin/python3

import logging
import sys
import fileinput
import csv
import time
import re
import statistics
import copy
from collections import Counter
from collections import deque
from functools import reduce

validpathcount = 0

def pdata(data):
    for p,val in data.items():
        for d in val['next']:
            print("{} -> {}".format(p, d))
        print("")

def spath(path):
    s = ""
    if len(path):
        s = "{}".format(path[0])
        for p in path[1:]:
            s += ",{}".format(p)
    return s

def issmallcavevalid(path):

    counts = {}
    # count the small caves
    for c in path:
        if (c == 'start') or (c == 'end'):
            continue
        if (c.islower()):
            if c in counts:
                counts[c] += 1
            else:
                counts[c] = 1
            if counts[c] > 2:
                logging.debug(" small cave path {} is invalid (more than 2): {}".format(path, counts))
                return False

    twocounts = 0
    for c in counts.values():
        if c >= 2:
            twocounts += 1

    if twocounts >= 2:
        logging.debug(" small cave path {} is invalid (multiple 2s): {}".format(path, counts))
        return False

    logging.debug(" small cave path {} is valid: {}".format(path, counts))
    return True

def findpaths(data, currentpath):

    global validpathcount
    point = currentpath[-1]
    logging.debug("{}findpaths({})".format(' '*len(currentpath), spath(currentpath)))

    # reached end
    if (point == 'end'):
        validpathcount += 1
        logging.debug("{}  Reached end. valid path: {}".format(' '*len(currentpath),spath(currentpath)))
        print("{:3d} valid path: {}".format(validpathcount, spath(currentpath)))
        return

    if (point.islower()):
        # Only hit 'start' once'
        if (point == 'start'):
            if (point in currentpath[1:]):
                logging.debug("{}  hit a repeated start cave ({} in {}): done".format(' '*len(currentpath), point, spath(currentpath[1:])))
                return
        # Only a single small caves twice, rest once
        else:
            #if ((currentpath[:-1].count(point)) >= 2):
            if not issmallcavevalid(currentpath):
#                logging.debug("{}  hit a small cave {} {} times: done".format(' '*len(currentpath), point, currentpath[:-1].count(point)))
                return

    data[point]['visited'] += 1
    for each in data[point]['next']:
        logging.debug("{}  recurse to: {}".format(' '*len(currentpath), spath(currentpath + [each])))
        findpaths(data, currentpath + [each])

def part1(data):

    findpaths(data, ["start"])

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    data = {}
    for line in fileinput.input():
        [a,b] = line.rstrip().split('-')
        logging.debug("[{}] - [{}]".format(a,b))

        if a not in data:
            data[a] = {'visited': 0, 'next': []}
        data[a]['next'].append(b)
        logging.debug("  added forward path {} -> {}".format(a,b))

        # Make sure the reverse path exists too
        if b not in data:
            data[b] = {'visited': 0, 'next': [a]}
            logging.debug("  created initial reverse path {} -> {}".format(b,a))
        elif a not in data[b]['next']:
            data[b]['next'].append(a)
            logging.debug("  added reverse path {} -> {}".format(b,a))
        else:
            logging.debug("  reverse path {} -> {} already exists".format(b,a))

    # sort the next paths so they match the examples
    for p,val in data.items():
        logging.debug("val[next]: {}".format(val['next']))
        val['next'].sort()

    logging.debug('Initial data:')
    pdata(data)

    before = time.time()
    result = part1(data)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

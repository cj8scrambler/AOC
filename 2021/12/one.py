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

validpathcount = 0

def pdata(data):
    for p,val in data.items():
        for d in val['next']:
            print("{} -> {}".format(p, d))
        print("")


def findpaths(data, currentpath):

    global validpathcount
    point = currentpath[-1]
    logging.debug("{}findpaths({}, {})".format(' '*len(currentpath), point, currentpath))

    # reached end
    if (point == 'end'):
        validpathcount += 1
        logging.debug("{}  Reached end. valid path: {}".format(' '*len(currentpath),currentpath))
        print("{:3d} valid path: {}".format(validpathcount, currentpath))
        return

    if (point.islower()):
        #if (data[point]['visited'] > 0):
        if (len(currentpath) > 1) and (point in currentpath[:-1]):
            logging.debug("{}  hit a repeated small/start cave ({} in {}): done".format(' '*len(currentpath), point, currentpath[:-1]))
            return

    data[point]['visited'] += 1
    for each in data[point]['next']:
        logging.debug("{}  recurse to: {}".format(' '*len(currentpath), currentpath + [each]))
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

    logging.debug('Initial data:')
    pdata(data)

    before = time.time()
    result = part1(data)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

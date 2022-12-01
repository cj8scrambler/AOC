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
import binascii
from heapq import heappush, heappop
from collections import deque
from collections import Counter
from functools import reduce

def pdata(data):

    return 0

def get_regular(index, term):
    if type(term[index]) == int:
        logging.debug("found a regular number at [{}]: {}".format(index,term[index]))
        return term[index]

    other = 1;
    if index == 1:
        other = 0;

    if type(term[other]) == int:
        logging.debug("found a regular number at [{}]: {}".format(other,term[other]))
        return term[other]

    # check the other side first of it's a list
    if type(term[other]) == list:
        return get_regular(other,term[other])

    if type(term[index]) == list:
        return get_regular(index,term[index])

def reduce(data, depth):

    depth += 1
    logging.debug("{}Reduce({}):".format(' '*depth, data))
    for side in [0, 1]:
        other = int(not side)
        if type(data[side]) == list:
            exploded = reduce(data[side], depth)
            if type(data[0]) == int:
                data[0] += exploded(0)
        if type(data[other]) == list:
            reduce(data[side], depth)

        if (type(data[0]) == int) and (type(data[1]) == int) and depth > 4:
            # Need to explode
            logging.debug("{}  element {} needs to explode".format(' '*depth, data))
            return tuple(data)

    if len(data) == 0:
        logging.debug("{}  At the end.".format(' '*depth))

    return 0

def part1(data):
    return 0

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    data = []
    for line in fileinput.input():
        exp = []
        elnum = 0
        for c in line.rstrip():
            #logging.debug("  c: '{}': exp: {}".format(c,exp))
            if c=='[':
                #logging.debug("  c: '{}': push new list".format(c))
                exp.append([])
            elif c.isdigit():
                #logging.debug("  c: '{}': add {} to last element".format(c, int(c)))
                exp[-1].append(int(c))
            elif c==']':
                last = exp.pop()
                #logging.debug("  c: '{}': pop and append)".format(c, last))
                if len(exp):
                    exp[-1].append(last)
                else:
                    logging.debug("Finished expression: {}".format(last))
                    data.append(last)
            
    logging.debug('data: {}'.format(data))
    for exp in data:
        reduce(exp, 0)

    before = time.time()
    result = part1(data)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

#    before = time.time()
#    (result,length) = handle_packet(data)
#    after = time.time()
#    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

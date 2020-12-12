#!/usr/bin/python

import logging
import sys
import fileinput
import time
import copy
from itertools import combinations 
  

def part1(data):
    ones = 0
    threes = 0
    for i in range(1, len(data)):
        delta = data[i] - data[i-1]
        logging.debug("  i=%d:  %d - %d  = %d" % (i, data[i], data[i-1], delta))
        if (delta == 1):
            ones += 1
        elif (delta == 3):
            threes += 1

    logging.debug("  ones=%d  threes=%d" % (ones, threes))
    return (ones * threes)

def validate(data):
    logging.info("    Validate: {0}".format(data))
    for i in range(1, len(data)):
        delta = data[i] - data[i-1]
        #logging.debug("    i=%d:  delta=%d invalid=%d" % (i, delta, (delta > 3)))
        if (delta >3):
            return False
    logging.error("    Valid sequence: {0}".format(data))
    return True

def try_without(data, n, sum):

    valid = 0
    trydata = copy.copy(data)
    trydata.pop(n)

    if (len(data) <= 2):
        return (valid, sum)

    logging.info("SUM={1} Try data original: {0}".format(trydata,sum))
    valid = validate(trydata)
    sum += valid

    for i in range(1, len(trydata)-1):
        logging.info("SUM={1} Try data loop: {0}".format(trydata,sum))
        (subvalid, sum) = try_without(trydata,i, sum)

    return (valid, sum)

def part2(data):
    logging.error("Part2 Initial data: {0}".format(data))
    sum=validate(data)
    for i in range(1, len(data)-1):
        (valid, sum) = try_without(data, i, sum)

    return sum

def part2d(data):
    # make a bucket for each possible adapter
    solution = [1]+[0]*data[-1]
    logging.debug("Arrange ({0} 0s: {1}".format(data[-1],solution))

    for i in data[1:]:
        solution[i] = solution[i-3] + solution[i-2] + solution[i-1]
    logging.debug("solution is: %d" % (solution[-1]))
    return solution[-1]

if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)

    data = [int(line) for line in fileinput.input()]
    data.append(0)
    data.append(max(data)+3)
    data.sort()
    logging.debug("Data: {0}".format(data));

    result = part1(data)
    print("Part 1:  product: %d" % (result))

    result = part2d(data)
    print("Part 2:  combos: %d" % (result))

#!/usr/bin/python

import logging
import sys
import fileinput
import time
from itertools import combinations 
  
def validate(data, val):
    combos = combinations(data, 2)
    for combo in combos:
        logging.debug("  On: {0} ({1})".format(combo, sum(combo)))
        if (sum(combo) == val):
            logging.debug("  Found match.")
            return True

    return False

def part1(data, n):
    logging.debug("part1() data: {0}  n: {1}".format(data, n))
    for offset in range(n, len(data)):
        logging.debug("Validate %d using %d-%d:" % (data[offset], offset-n, offset-1))
        if not validate(data[offset-n:offset], data[offset]):
            logging.info("Found invalid value %d:" % data[offset])
            return data[offset]

def part2(data, val):
    for a in range(len(data)):
        for b in range(a+1, len(data)):
            thesum = sum(data[a:b+1])
            logging.debug("  range %d-%d: %d..+..%d = %d (looking for %d)" %
                          (a, b, data[a], data[b], thesum, val))
            if (thesum == val):
                logging.info("Found match: %d (#%d)...%d (#%d)" % (data[a], a, data[b], b))
                logging.debug("  min from range %d-%d: %d" % (a, b, min(data[a:b])))
                logging.debug("  max from range %d-%d: %d" % (a, b, max(data[a:b])))
                return min(data[a:b]) + max(data[a:b])
            if (thesum > val):
                logging.debug("Too high; move on")
                break;

    # should not hit this
    return None

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    window = 25
    data = [int(line) for line in fileinput.input()]

    before = time.time()
    result = part1(data, window)
    after = time.time()
    print("part 1: %d (%f seconds)" % (result, after-before))

    before = time.time()
    result = part2(data, result)
    after = time.time()
    print("part 2: %d (%f seconds)" % (result, after-before))

#!/usr/bin/python

import logging
import sys
import fileinput
import time
from itertools import combinations 

def value(letter):

    l = ord(letter)

    # lower case
    if l > 90:
        v = l - 96
    # uppoer case
    else:
        v = l - 38

    logging.debug("score of {}: {}".format(letter, v))
    return v

  
def part2(data):

    total = 0

    while (len(data)):
        e1 = set(data.pop(0).strip())
        e2 = set(data.pop(0).strip())
        e3 = set(data.pop(0).strip())
        logging.debug("e1: '{}'  e2: '{}'  e3: '{}'".format(e1,e2,e3))
        for c in e1 & e2 & e3:
            logging.debug("  found a common match: {}".format(c))
            total += value(c)
            logging.debug("  new total: {}".format(total))
            
    logging.debug("  done return total: {}".format(total))
    return(total)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    lines = [line for line in fileinput.input()]

#    before = time.time()
#    result = part1(lines)
#    after = time.time()
#    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

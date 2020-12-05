#!/usr/bin/python

import logging
import sys
import fileinput
import time
from itertools import combinations 
  
def showme(data):
    for line in data:
        logging.info("{0}".format(line))

def findseat(loc):
    ROW = (0, 127)
    COL = (0, 7)
    logging.debug("findseat for: '%s'" % (loc))
    for r in loc[0:7]:
        logging.debug("Row code: %c" % (r))
        ROW = bisect(ROW, r)
    if (ROW[0] != ROW[1]):
        print("Row did not converge: %d-%d", ROW[0], ROW[1])
        raise

    for c in loc[7:10]:
        logging.debug("Col code: %c" % (c))
        COL = bisect(COL, c)
    if (COL[0] != COL[1]):
        print("Column did not converge: %d-%d", COL[0], COL[1])
        raise

    logging.info("%s: row %d, col %d, seat ID %d" %
                 (loc, ROW[0], COL[0], 8 * ROW[0] + COL[0]))
    return (8 * ROW[0] + COL[0])

def bisect(the_range, letter):
    if letter == 'F' or letter == 'L':
#        logging.debug("  (%d + %d) / 2 => %d" % (the_range[1], the_range[0], (the_range[1]+the_range[0])/2))
        result = (the_range[0], (the_range[1]+the_range[0])/2)
    elif letter == 'B' or letter == 'R':
        result = ((the_range[1]+the_range[0])/2+1, the_range[1])
#        logging.debug("  ((%d + %d) / 2) + 1=> %d" % (the_range[1], the_range[0], (the_range[1]+the_range[0])/2 + 1))
    else:
        logging.error("Invalid bisect letter: %c" % (letter))

    logging.debug("bisect({0}, {1}) -> {2}".format(the_range, letter, result))

    return result

if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)

    data = [i.rstrip() for i in fileinput.input()]

    #showme(data)
    found = []
    for loc in data:
        found.append(findseat(loc))

    found.sort()
    print ("Part 1: highest seat ID: %d " % max(found))

    last = found[0]-1
    for seat in found:
        if (seat - 1) != last:
            print("Part 2: missing seat between: %d - %d" % (last, seat))
        last = seat;

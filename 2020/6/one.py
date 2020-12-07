#!/usr/bin/python

import logging
import sys
import fileinput
import time
import re
from itertools import combinations 
  
def showme(data):
    for line in data:
        logging.info("  {0}".format(line))

def part1_count_yeses(data):
    logging.debug("  Count Yeses in: {0}".format(data))
    ormap = {}
    for person in data:
        for q in person:
            ormap[q] = ormap.setdefault(q, 0) + 1

    logging.debug("  Yes map {0}".format(ormap))
    logging.debug("  Yes value: %d" % (len(ormap.keys())))
    return len(ormap.keys())

def part2_count_yeses(data):
    groupsize = len(data)
    logging.debug("  Count Yeses {0} size group: {1}".format(groupsize, data))
    ormap = {}
    for person in data:
        for q in person:
            ormap[q] = ormap.setdefault(q, 0) + 1

    yes = 0;
    for q in ormap:
        if ormap[q] == groupsize:
            logging.debug("  Q '%c': yes (%d)" % (q, ormap[q]))
            yes += 1
        else:
            logging.debug("  Q '%c': no (%d)" % (q, ormap[q]))

    logging.debug("  Total yes: %d" % (yes))
    return yes

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    data = []
    total = 0
    for line in fileinput.input():
        logging.debug("line: '%s'" % (line))
        if line == "\n":
            logging.debug("Process data");
            # Process previous record
            v = part2_count_yeses(data)
            total += v
            data = []
        else:
            logging.debug("Line as list of chars: {0}".format(list(line.rstrip())))
            data.append(list(line.rstrip()))

    print("Part 2 yeses: %d" % (total))

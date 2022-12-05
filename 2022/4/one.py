#!/usr/bin/python

import logging
import sys
import fileinput
import time
from itertools import combinations 

def part1(data):

    total = 0

    for line in data:
        [r1, r2] = line.split(',')
        r1b,r1e = r1.split('-')
        r2b,r2e = r2.split('-')
        logging.debug("elf1: {}-{}  elf2: {}-{}".format (r1b, r1e, r2b, r2e))
        s1 = set(range(int(r1b),int(r1e)+1))
        s2 = set(range(int(r2b),int(r2e)+1))
        logging.debug("set1: {}  set2:{}".format (s1, s2))
        if s1.union(s2) == s1:
            logging.debug("set2: wholy within set1")
            total += 1
        elif s2.union(s1) == s2:
            logging.debug("set1: wholy within set2")
            total += 1

    return(total)

def part2(data):

    total = 0

    for line in data:
        [r1, r2] = line.split(',')
        r1b,r1e = r1.split('-')
        r2b,r2e = r2.split('-')
        logging.debug("elf1: {}-{}  elf2: {}-{}".format (r1b, r1e, r2b, r2e))
        s1 = set(range(int(r1b),int(r1e)+1))
        s2 = set(range(int(r2b),int(r2e)+1))
        logging.debug("set1: {}  set2:{}".format (s1, s2))
        if len(s1.intersection(s2)) > 0:
            logging.debug("set1 and two overlap")
            total += 1

    return(total)


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    lines = [line for line in fileinput.input()]

    before = time.time()
    result = part1(lines)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

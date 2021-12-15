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
from collections import Counter
from functools import reduce

def step(rules, begin):

    new = []
    for i in range(len(begin)-1):
        p = (begin[i], begin[i+1])
        logging.debug("pair-{}: {}".format(i, p))
        if i == 0:
            new.append(p[0])
        new.append(rules[p])
        new.append(p[1])
        logging.debug("  {}".format(new))

    return new

# Takes a Counter() of char pairs and returns a Counter() of the individual cars
def char_counts(counter, firstletter):

    chars = Counter()
    chars[firstletter] += 1
    for pair in counter:
        chars[pair[1]] += counter[pair]

    logging.debug("Counts of: {}".format(counter))
    logging.debug("      are: {}".format(chars))
    return chars


# completely re-write
def part2(rules, begin, steps):

    before = time.time()
    firstletter = begin[0]  # needed for counts later.  1st letter never changes
    counts = Counter()      # for itterating over
    newcounts = Counter()   # copy of counts for updating (without breaking itterator)

    # Initial pair counts:
    for i in range(len(begin)-1):
        pair = tuple(begin[i:i+2])
        newcounts[pair] += 1
    logging.debug("initial pair newcounts: {}".format(newcounts))

    for s in range(steps):
        counts = copy.copy(newcounts)
        logging.debug("Step-{}".format(s+1))
        for pair in counts.keys():
            logging.debug("  pair-{}: insert: {}  ({} times)".format(pair, rules[pair], counts[pair]))
            newcounts[(pair[0], rules[pair])] += counts[pair]
            newcounts[(rules[pair], pair[1])] += counts[pair]
            newcounts[pair] -= counts[pair]
            logging.debug("  pair-{}: i-{} newcounts: {}".format(pair, i, newcounts))
            logging.debug("")
        logging.debug("step-{}: new counts: {}".format(s+1, newcounts))

        cc = char_counts(newcounts, firstletter)
        logging.info("{:.1f}: step-{}: new character counts: {}".format(time.time()-before, s+1, cc))

    minc = min(cc, key=cc.get)
    maxc = max(cc, key=cc.get)
    logging.info("{:.1f}: Min: {}: {}   Max: {}: {}  Diff: {}".format(time.time()-before, minc, cc[minc], maxc, cc[maxc], cc[maxc] - cc[minc]))
    return (cc[maxc] - cc[minc])

def part1(rules, begin, steps):

    before = time.time()
    for s in range(steps):
        begin = step(rules, begin)
        #logging.info("After step-{}: len={}  {}".format(s+1, len(begin), "".join(begin)))
        logging.info("{:.1f}: step-{}: len={}".format(time.time()-before, s+1, len(begin)))

    counts = Counter(begin)
    logging.debug("counts: {}".format(counts))
    minc = min(counts, key=counts.get)
    maxc = max(counts, key=counts.get)
    logging.info("{:.1f}: Min: {}: {}   Max: {}: {}  Diff: {}".format(time.time()-before, minc, counts[minc], maxc, counts[maxc], counts[maxc] - counts[minc]))
    return (counts[maxc] - counts[minc])

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    rules = {}
    for line in fileinput.input():
        g = re.match( r"^([A-Z])([A-Z]) -> ([A-Z])$", line)
        if g:
            rules[(g.group(1), g.group(2))] = g.group(3)
        elif len(line) > 1:
            begin = list(line.rstrip())

    logging.debug('begin: {}'.format(begin))
    logging.debug('rules: {}'.format(rules))

    before = time.time()
    result = part1(rules, begin, 10)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(rules, begin, 40)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

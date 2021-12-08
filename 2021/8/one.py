#!/usr/bin/python3

import logging
import sys
import fileinput
import csv
import time
import re
import statistics
import copy
from functools import reduce

# number of segments in each number display
dlen = {0: 6,
        1: 2, #unique
        2: 5,
        3: 5,
        4: 4, #unique
        5: 5,
        6: 6,
        7: 3, #unique
        8: 7, #unique
        9: 6 }

# Just the unique lengths
ulen = {2: 1,
        4: 4,
        3: 7,
        7: 8}

# Didn't end up using this map
rules = {0: ['a', 'b', 'c', 'e', 'f', 'g'],
         1: ['c', 'f'],
         2: ['a', 'c', 'd', 'e', 'g'],
         3: ['a', 'c', 'd', 'f', 'g'],
         4: ['b', 'c', 'd', 'f'],
         5: ['a', 'b', 'd', 'f', 'g'],
         6: ['a', 'b', 'd', 'e', 'f', 'g'],
         7: ['a', 'c', 'f'],
         8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
         9: ['a', 'b', 'c', 'd', 'f', 'g'] }


def part1(data):

    logging.debug("part1 data: {}".format(data))

    count=0
    for i,d in enumerate(data):
        for o in d['out']:
            if (len(o) == 2): #1
                count += 1
                logging.debug("output-{} '{}' count={}".format(i, o, count))
            if (len(o) == 4): #4
                count += 1
                logging.debug("output-{} '{}' count={}".format(i, o, count))
            if (len(o) == 3): #7
                count += 1
                logging.debug("output-{} '{}' count={}".format(i, o, count))
            if (len(o) == 7): #8
                count += 1
                logging.debug("output-{} '{}' count={}".format(i, o, count))

    return count

def part2(data):

    results = [None] * 10
    lengths = [ [] for i in range(10)]
    sum = 0

    for i,line in enumerate(data):
        # Get the length of each entry and save the unique ones
        for o in line['in']:
            lengths[len(o)].append(set(o))
            if (len(o) in ulen):
                results[ulen[len(o)]] = set(o)
                logging.debug("line-{} '{}' is unique. results[{}]: {}".format(i, o, ulen[len(o)], results[ulen[len(o)]]))
    
        # Figure out non-unique digits

        # Among 5 segment numbers only 3 works for: n = n | '1' 
        for n in lengths[5]:
            if n | results[1] == n:
                logging.debug("set {} must be '3'".format(n))
                results[3] = n

        # Among 6 segment numbers only 6 works for: n - '1' = '8' - '1' 
        for n in lengths[6]:
            if n - results[1] == results[8] - results[1]:
                logging.debug("set {} must be '6'".format(n))
                results[6] = n

        # 9 is: '3' | '4' (and it's a 6 segment number)
        for n in lengths[6]:
            if n == (results[3] | results[4]):
                logging.debug("set {} must be '9'".format(n))
                results[9] = n

        # The unknown 6 segment must be '0'
        for n in lengths[6]:
            if n not in results:
                logging.debug("set {} must be '0'".format(n))
                results[0] = n

        # Among 5 segment numbers only 5 works for: n | 1 == n | 1 | 4
        for n in lengths[5]:
            if n | results[1] == n | results[1] | results[4]:
                logging.debug("set {} must be '5'".format(n))
                results[5] = n

        # The unknown 5 segment must be '2'
        for n in lengths[5]:
            if n not in results:
                logging.debug("set {} must be 's'".format(n))
                results[2] = n

        logging.debug("results: {}".format(results))

#        # Now figure out each sgement (turns out this was never needed)
#
#        # '7' - '1' is the a segment
#        a = (results[7] - results[1]).pop()
#        translate[ord(a)] = ord('a')
#        logging.debug("r[7] - r[1]: a -> {}  translate: {}".format(results[7] - results[1], translate))
#
#        # '4' - '3' is the b segment
#        b = (results[4] - results[3]).pop()
#        translate[ord(b)] = ord('b')
#        logging.debug("r[4] - r[3]: b -> {}  translate: {}".format(results[4] - results[3], translate))
#
#        # '8' - '6' is the c segment
#        c = (results[8] - results[6]).pop()
#        translate[ord(c)] = ord('c')
#        logging.debug("r[8] - r[6]: c -> {}  translate: {}".format(results[8] - results[6], translate))
#
#        # '8' - '0' is the d segment
#        d = (results[8] - results[0]).pop()
#        translate[ord(d)] = ord('d')
#        logging.debug("r[8] - r[0]: d -> {}  translate: {}".format(results[8] - results[0], translate))
#
#        # '3' - '2' is the f segment
#        f = (results[3] - results[2]).pop()
#        translate[ord(f)] = ord('f')
#        logging.debug("r[3] - r[2]: f -> {}  translate: {}".format(results[3] - results[2], translate))
#
#        # '3' - '4' -'7' is the g segment
#        g = (results[3] - results[4] - results[7]).pop()
#        translate[ord(g)] = ord('g')
#        logging.debug("r[3] - r[4] - r[7]: g -> {}  translate: {}".format(results[3] - results[4] - results[7], translate))

        # Now convert the reults from sets to alpha sorted string sequences
        for i,r in enumerate(results):
            s = list(r)
            s.sort()
            results[i] = ''.join(s)
        logging.debug("sorted string results: {}".format(results))

        output = ""
        # Now translate the outputs:
        for o in line['out']:
            s = list(o)
            s.sort()
            m = ''.join(s)
            for i,r in enumerate(results):
                if m == r:
                    output += "{}".format(i)
                    logging.debug("  {}: {}  {}".format(o,i, output))
        sum += int(output)
        logging.info("{}: {}  sum: {}".format(line['out'], output, sum))

    return sum

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    data = []
    inp = fileinput.input()
    for line in fileinput.input():
        (input, output) = line.split('|')
        data.append({'in': input.split(), 'out': output.split()})

    logging.debug('Initial data: {})'.format(data))

    before = time.time()
    result = part1(data)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(data)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

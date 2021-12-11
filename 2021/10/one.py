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

# Map of matching pairs (forward/reverse)
fmap = { '[': ']', '{': '}', '(': ')', '<': '>'}
rmap = { ']': '[', '}': '{', ')': '(', '>': '<'}

scores1 = {')': 3, ']': 57, '}': 1197, '>': 25137}
scores2 = {')': 1, ']': 2, '}': 3, '>': 4}

def part1(data):

    score = 0
    for l,line in enumerate(data):
        invalid = False
        stack = deque()
        for c in line:
            if c in fmap.keys():
                stack.append(c)
                logging.debug("  new pair started with {}".format(c))
            elif stack and (stack[-1] == rmap[c]):
                p = stack.pop()
                logging.debug("  closed {} with {}".format(p, c))
            else:
                score += scores1[c]
                logging.info("line-{}: invalid char: {}  score: {}  total score: {}".format(l,c,scores1[c],score))
                invalid = True;
                break;

        if not invalid:
            if stack:
                logging.info("line-{}: incomplete; skip".format(l))
            else:
                logging.info("line-{}: valid".format(l))

    return score

def part2(data):

    linescores = []
    for l,line in enumerate(data):
        stack = deque()
        corrupt = False
        for ic,c in enumerate(line):
            if c in fmap.keys():
                stack.append(c)
                logging.debug("    new pair started with {}".format(c))
            elif stack and (stack[-1] == rmap[c]):
                p = stack.pop()
                logging.debug("    closed {} with {}".format(p, c))
            else:
                logging.debug("line-{}: corrupt; invalid char: {}; marked corrupt".format(l,c))
                corrupt = True;
                break;

        if not corrupt:
            if stack:
                linescores.append(0)
                solution = []
                logging.debug("line-{}: incomplete; stack: {}".format(l, stack))
                while stack:
                    solution.append(fmap[stack.pop()])
                    linescores[-1] = 5 * linescores[-1] + scores2[solution[-1]]
                    logging.debug("  added {} for {}; total score: {}".format(solution[-1], scores2[solution[-1]], linescores[-1]))
                logging.info("line-{} solution: {}  score: {}".format(l, solution, linescores[-1]))
            else:
                logging.info("line-{}: valid".format(l))

    linescores.sort()
    logging.debug("sorted linescores ({}): {}".format(len(linescores),linescores))
    if len(linescores):
        logging.debug("middle score: {}".format(linescores[int(len(linescores)/2)]))
        return linescores[int(len(linescores)/2)]

    return 0;


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    data = []
    for line in fileinput.input():
        data.append(line.rstrip())

    logging.debug('Initial data: {})'.format(data))

#    before = time.time()
#    result = part1(data)
#    after = time.time()
#    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(data)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

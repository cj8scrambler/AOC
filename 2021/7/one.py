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

def part1(data):
    logging.debug("part1 data: {}".format(data))
    median = statistics.median(data)

    fuel = 0
    for i,c in enumerate(data):
        fuel += abs(c - median)
        logging.debug("  crab-{} {} setps to {} (total: {})".format(i, abs(c-median), median, fuel))

    return fuel

def triangle_cost(data, point):
    fuel = 0
    for i,c in enumerate(data):
        fc = 0
        for f in range(int(abs(c-point)+1)):
            logging.debug
            fc+=f
        
        fuel += fc
        logging.debug("  crab-{} {} setps to {} (cost: {}) (total: {})".format(i, abs(c-point), point, fc, fuel))
    return fuel


def part2(data):
    logging.debug("part2 data ({} elements): {}".format(len(data), data))
    costs = [-1] * len(data)

    # Start off with the cost at the mean point
    mean = int(round(statistics.mean(data)))
    costs[mean] = triangle_cost(data,mean)
    logging.info("Mean is {} cost[{}]: {}".format(mean, mean, costs[mean]))

    # Decide if mean, left or right is best
    if mean > 0:
        costs[mean-1] = triangle_cost(data,mean-1);
        left_delta = costs[mean]-costs[mean-1]
    else:
        left_delta = -1

    if mean < (len(data) - 1):
        costs[mean+1] = triangle_cost(data,mean+1);
        right_delta = costs[mean]-costs[mean+1]
    else:
        right_delta = -1

    if (left_delta < 0) and (right_delta < 0):
        logging.info("Mean was the best cost")
        return costs[mean]

    # Keep searching in that same direction
    if left_delta > right_delta:
        direction = -1
        delta = left_delta
        logging.info("Left side was better cost[{}]: {} (delta: {})".format(mean-1, costs[mean-1], delta))
    else:
        direction = +1
        delta = right_delta
        logging.info("Right side was better cost[{}]: {}".format(mean+1, costs[mean+1], delta))

    # Done 3 itterations on data so far
    count = 3
    offset = mean + direction
    while (delta > 0):
        offset += direction
        costs[offset] = triangle_cost(data,offset);
        delta = costs[offset-direction] - costs[offset]
        logging.info("cost[{}]: {}  (delta: {})".format(offset, costs[offset], delta))
        count += 1

    logging.info("Best cost[{}]: {} (took {} itterations)".format(offset-direction, costs[offset-direction], count))

    return costs[offset]

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    inp = fileinput.input()
    try:
        data = [int(i) for i in next(inp).rstrip().split(',')]
    except:
        print("Unable to read data")
        sys.exit(1)

    logging.debug('Initial data: {})'.format(data))

    before = time.time()
    result = part1(data)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(data)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

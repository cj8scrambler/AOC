#!/usr/bin/python3

import logging
import sys
import fileinput
import csv
import time
import re
import copy
from functools import reduce

def part1(data, days):
    logging.debug("part1 data: {}".format(data))
    for day in range(1, days+1):
        logging.debug("Begin day-{}".format(day))

        newfish = 0
        for i,age in enumerate(data):
            logging.debug("  day[{}] fish[{}]: {} ({})".format(day, i, age, type(age)))
            if age > 0:
                data[i] -= 1
            else:
                data[i] = 6
                newfish += 1

        for i in range(newfish):
            data.append(8)
        logging.debug("After {} days: {}".format(day, data))
        if ((day % 10) == 0):
            logging.error("Finished day{}".format(day))
    logging.info("After {} days: {} fish".format(days, len(data)))
    return len(data)

def part2(data, days):
    counts = [0] * 9;
    last = time.time()
    for f in data:
        counts[f] += 1

    for day in range(1, days+1):
        logging.debug("Day-{}".format(day))
        d0 = counts.pop(0)
        counts.append(0)
        counts[6] += d0
        counts[8] += d0
        logging.debug("  end of day counts: {}".format(counts))

    logging.info("After {} days: {} fish: {}".format(days, sum(counts), counts))
    return sum(counts)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    inp = fileinput.input()
    try:
        fish = [int(i) for i in next(inp).rstrip().split(',')]
    except:
        print("Unable to read data")
        sys.exit(1)

    logging.debug('Initial fish: {})'.format(fish))

    before = time.time()
    result = part2(copy.copy(fish),80)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(fish, 256)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

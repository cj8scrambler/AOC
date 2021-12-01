#!/usr/bin/python

import logging
import sys
import fileinput
import time
from itertools import combinations 
  
def count_inc(data):
    last = None
    inc = 0
    for l in data:
        if last and int(l) > last:
            inc += 1
        last = int(l)

        logging.debug("line: {} : {}".format(int(l), inc))

    logging.debug("return {}".format(inc))
    return(inc)

def count_inc_window3(data):
    window = 0
    last = None
    inc = 0
    sums = []
    for l in data:
        sums.append(l)
        if window > 0:
            sums[window-1] = sums[window-1] + l
        if window > 1:
            sums[window-2] = sums[window-2] + l
        if window > 2:
            new = sums[window-3]
            if last and new > last:
                inc += 1
            last = new
            logging.debug("line-{}: value={} last={} inc={} sums: {}".format(window, l, last, inc, sums))

        window += 1

    new = sums[window-3]
    if last and new > last:
        inc += 1
    last = new
    logging.debug("line-{}: value={} last={} inc={} sums: {}".format(window, l, last, inc, sums))

    return(inc)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [int(line) for line in fileinput.input()]

    before = time.time()
    result = count_inc(lines)
    after = time.time()
    print("part 1 increments: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = count_inc_window3(lines)
    after = time.time()
    print("part 2 increments with window=3: {} ({:.3f} sec)".format(result, (after - before)))

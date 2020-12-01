#!/usr/bin/python

import logging
import sys
import fileinput
import time
from itertools import combinations 
  
def combo_2020(data, n):
    combos = combinations(data, n)
    for combo in combos:
        logging.debug("  On: {0}".format(combo))
        if (sum(combo) == 2020):
            logging.debug("  Found match.")
            product = 1
            for each in combo:
                logging.debug("  %d * %d = %d" % (product, each, product*each))
                product *= each
            return(product)

def two_2020(data):
    start = 0;
    for line in data:
        logging.debug("%d" % (line))
        for i in range(start, len(data)):
            logging.debug("  %d : %d" % (data[i], line+data[i]))
            if ((line + data[i]) == 2020):
                logging.debug("Found match: %d + %d = 2020" % (line, data[i]))
                return(line * data[i])
        start += 1

def three_2020(data):
    for line in data:
        logging.debug("%d" % (line))
        start = 0;
        for i in range(len(data)):
            logging.debug("  %d" % (data[i]))
            for j in range(start, len(data)):
                logging.debug("    %d : %d" % (data[j], line+data[i]+data[j]))
                if ((line + data[i] + data[j]) == 2020):
                    logging.debug("Found match: %d + %d +%d = 2020" % (line, data[i], data[j]))
                    return(line * data[i] * data[j])
            start += 1

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [int(line) for line in fileinput.input()]

    before = time.time()
    result = two_2020(lines)
    after = time.time()
    print("manual 2: %d (%f seconds)" % (result, after-before))

    before = time.time()
    result = combo_2020(lines,2)
    after = time.time()
    print("combo 2: %d (%f seconds)" % (result, after-before))

    before = time.time()
    result = three_2020(lines)
    after = time.time()
    print("manual 2: %d (%f seconds)" % (result, after-before))

    before = time.time()
    result = combo_2020(lines,3)
    after = time.time()
    print("combo 3: %d (%f seconds)" % (result, after-before))

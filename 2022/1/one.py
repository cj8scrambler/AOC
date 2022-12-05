#!/usr/bin/python

import logging
import sys
import fileinput
import time
from itertools import combinations 
  
def count_cals(data):
    cals = [0]

    for line in data:
        logging.debug("on line: '{}'".format(line.strip()))
        if line.strip() == "":
            cals.append(0)
            logging.debug("Encountered new elf # {}".format(len(cals)))
        else:
            cals[-1] += int(line)
            logging.debug("Updated elf {} to {}".format(len(cals), cals[-1]))
        
    return(max(cals))

def top3_cals(data):
    cals = [0]

    for line in data:
        logging.debug("on line: '{}'".format(line.strip()))
        if line.strip() == "":
            cals.append(0)
            logging.debug("Encountered new elf # {}".format(len(cals)))
        else:
            cals[-1] += int(line)
            logging.debug("Updated elf {} to {}".format(len(cals), cals[-1]))
        
    logging.debug("data: {}".format(cals))
    ints = [int(i) for i in cals]
    logging.debug("ints: {}".format(ints))
    ints.sort(reverse=True)
    logging.debug("sorted data: {}".format(ints))

    logging.debug("elf #1: {}".format(ints[0]))
    logging.debug("elf #2: {}".format(ints[1]))
    logging.debug("elf #3: {}".format(ints[2]))
    
    return(ints[0] + ints[1] + ints[2])

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [line for line in fileinput.input()]

    before = time.time()
    result = count_cals(lines)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = top3_cals(lines)
    after = time.time()
    print("part 2 top 3 sum: {} ({:.3f} sec)".format(result, (after - before)))

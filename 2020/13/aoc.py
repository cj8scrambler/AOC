#!/usr/bin/python

import logging
import sys
import fileinput
import time
import math
import re
from itertools import combinations 
  
def part1(time, data):

    nextbus=time
    while True:
        for bus in data:
            if bus != 'x':
                logging.debug("  try: %d  bus: %s  rem: %d" % (nextbus, bus, nextbus % int(bus)))
                if ((nextbus % int(bus)) == 0):
                    logging.debug(" Found match:  bus: %s  at time %d" % (bus, nextbus))
                    logging.debug("return (%d - %d) * %d: %d" % (nextbus, time, int(bus), (nextbus-time) * int(bus)))
                    return (nextbus-time) * int(bus)
        nextbus += 1
    return None

timestamp = 100000000000000
timestamp = 210600000000000

def verify(data):
    global timestamp
    #logging.debug("verify: bus {0} at {1} for {2}".format(data[0], timestamp, data))
    if (len(data) == 0):
        logging.info("  Got to the end: Success")
        return True
    elif (data[0] == 'x'):
        logging.debug("  got 'x' move ahead)")
        timestamp += 1
        return verify(data[1:])
    else:
        if (timestamp % int(data[0])) == 0:
            timestamp += 1
            logging.debug("  it's valid; move ahead")
            return verify(data[1:])
        else:
            return False

    return None

def part2(data):
    global timestamp
    logging.debug("TOP: start over a: timestamp=%d" % (timestamp))
    now = 0
    last = time.time()
    while not verify(data):
        timestamp += 1;
        if (timestamp % 10000000) == 0:
            now = time.time()
            logging.error("%d M (%.1f sec)" % (timestamp/1000000, now - last))
            last = now
    return True

if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)

    departure = 0
    data = []
    for line in fileinput.input():
        if departure == 0:
            departure = int(line)
            logging.debug("departure: {0}".format(departure))
        else:
            data = line.rstrip().split(",")
            logging.debug("data: {0}".format(data))

    #showme(data)
    result = part1(departure, data)
    print("Part1: %d" % result)
    result = part2(data)
    print("Part2 {0}".format(timestamp))

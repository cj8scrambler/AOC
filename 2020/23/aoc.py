#!/usr/bin/python3

import logging
import sys
import fileinput
import time
import math
import re
import copy
from itertools import combinations 
from itertools import permutations 

def move(data, current):

    mod = len(data)
    high = max(data)

    logging.info("current: {} [{}]".format(current, (data.index(current))))
    logging.info("cups: {}".format(data))

    current_i = data.index(current)
    #logging.debug("  pop ({}+1)%{}: data[{}] from {} = {}".format(current_i, len(data), (current_i+1) % len(data), data, data[(current_i+1) % len(data)]))
    bunch = [data.pop((current_i+1) % len(data))]

    current_i = data.index(current)
    #logging.debug("  pop ({}+1)%{}: data[{}] from {} = {}".format(current_i, len(data), (current_i+1) % len(data), data, data[(current_i+1) % len(data)]))
    bunch.append(data.pop((current_i+1) % len(data)))

    current_i = data.index(current)
    #logging.debug("  pop ({}+1)%{}: data[{}] from {} = {}".format(current_i, len(data), (current_i+1) % len(data), data, data[(current_i+1) % len(data)]))
    bunch.append(data.pop((current_i+1) % len(data)))
    logging.info("pick up: {}".format(bunch))

    i = None
    target = current - 1
    while i is None:
        logging.debug("    look for {} ({}-1)".format(target,target+1))
        try:
            i = data.index(target) % mod
        except ValueError:
            target -= 1
            if target < 0:
                target = high

    logging.debug("  found index of insert point: {}".format(i))
    logging.info("destination: {} [{}]".format(data[i],i))

    while (len(bunch)):
        i = (i + 1) % mod
        logging.debug("  insert {} at index {}".format(bunch[0], i))
        data.insert(i, bunch.pop(0))
        logging.debug("  bunch: {}  data: {}".format(bunch, data))

    current_i = data.index(current)
    ret_i = (current_i + 1) % mod
    logging.debug("  done; current {} [{}]; return {} [{}]".format(current, current_i, data[ret_i], ret_i))
    return data[ret_i]


def part1(data, moves):

    current = data[0]
    m = 1
    last = time.time()
    while m <= moves:
        logging.error("-- move {} --".format(m))
        current = move(data, current)
        m += 1
        logging.info("")
        if (m % 10) == 0:
            now = time.time()
            rate = 10.0 / (now - last)
            logging.error("Rate: {} / second".format(rate))
            logging.error("will finish in {} hours".format(((moves/rate)/60/60)))
            raise ValueError

    logging.info("-- final --".format(m))
    logging.info("cups: {}".format(data))

    result = ""
    i = (data.index(1) + 1) % len(data)
    for j in range(len(data)-1):
        result += str(data[i])
        i = (i + 1) % len(data)

    logging.info("Part1: {}".format(result))

    return result

if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)

    playerpat = re.compile(r"^Player ([\d]+):$")

    data = []

    for line in fileinput.input():
        data = [int(i) for i in list(line.rstrip())]

    logging.debug("Data: {}".format(data))

    #result = part1(data, 100)
    #print("Part1: {}".format(result))

    target = 1000000
    last = max(data)
    for i in range(len(data), target):
        last += 1
        data.append(last)

    result = part1(data, 10000000)

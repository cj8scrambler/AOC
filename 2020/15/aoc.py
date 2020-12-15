#!/usr/bin/python

import logging
import sys
import fileinput
import time
import re
from itertools import combinations 
  
def part1(data, limit):

    turn = 1
    history = {}
    last = 0

    # First turns are just saying the numbers in the data set
    for each in data:
        last = each
        history[last] = [turn]
        logging.info("turn {0}: say: {1}".format(turn, last))
        turn += 1

    # Now apply the rules of the game
    while turn <= limit:
        logging.debug("turn {0}".format(turn))
        # If there are 2 previous occurances of "last", then say the diff of the turn numbers that said them
        if last in history and (len(history[last]) > 1):
            logging.debug("  turn {0}: {1} has history > 1: {2}".format(turn, last, history[last]))
            logging.debug("     say %d - %d : %d" % (history[last][-1], history[last][-2], history[last][-1] - history[last][-2]))
            last = history[last][-1] - history[last][-2]
        # otherwise say 0
        else:
            logging.debug("  turn {0}: not enough history on {1}; say 0".format(turn, last))
            last = 0

        # Update the history tracker; only keep the last 2 occurances
        if (last in history):
            history[last] = [history[last][-1], turn]
        else:
            history[last] = [turn]

        logging.info("turn {0}: say: {1}".format(turn, last))

        # Print out progress every 1M turns
        if (turn % 1000000) == 0:
            logging.error("turn {0}: say: {1}".format(turn, last))

        turn += 1

    return last


if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)

    line = fileinput.input().next()
    data = [int(num) for num in line.rstrip().split(',')]

    #logging.debug("data: {0}".format(data))
    result = part1(data, 2020)
    print("Part1: %d" % result)

    # apparently the part1 solution can be re-used for part2 today
    result = part1(data, 30000000)
    print("Part2 %d" % result)

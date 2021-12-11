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

def check_neighbors(data, y, x):
    logging.debug("  Check neighbors of [{}][{}]".format(y,x))
    for ly in range(y-1,y+2):
        if ly >= 0 and ly < len(data):
            for lx in range(x-1,x+2):
                if lx >= 0 and lx < len(data[ly]):
                    if not ((lx == x) and (ly == y)):
                        data[ly][lx] += 1
                        logging.debug("  [{}][{}] neighbor now {}".format(ly,lx,data[ly][lx]))
                        if data[ly][lx] == 10:
                            logging.debug("  [{}][{}] FLASH".format(ly,lx))
                            check_neighbors(data, ly, lx)
                    else:
                        logging.debug("  skip myself: [{}][{}]".format(ly,lx))
                else:
                    logging.debug("  skip invalid neighbor (x): [{}][{}]".format(ly,lx))
        else:
            logging.debug("  skip invalid neighbor (y): [{}][?]".format(ly))

def pdata(data):
    for y,row in enumerate(data):
        for x,val in enumerate(row):
            if val < 10:
                print("{}".format(val), end='')
            else:
                print("#", end='')
        print("")

def parts(data, steps):

    total_flashes= 0;
    step = 0
    while True:
        step_flashes = 0;
        for y,row in enumerate(data):
            for x,val in enumerate(row):
                data[y][x] += 1
                if data[y][x] == 10:
                    logging.debug("  [{}][{}] FLASH".format(y,x))
                    check_neighbors(data, y, x)
#        logging.debug("End of step-{}:".format(step))
#        pdata(data)

        for y,row in enumerate(data):
            for x,val in enumerate(row):
                if val >= 10:
                    data[y][x] = 0
                    step_flashes += 1
                    total_flashes += 1

        step += 1
        if (step == steps):
            print("Part 1: total_flashes after {} steps: {}".format(total_flashes, steps))

        if (len(data) * len(data[0]) == step_flashes):
            logging.debug("Part 2: step-{} has all flashing".format(step))
#            pdata(data)
            return step
        else:
            logging.debug("End of step-{}: step_flashes: {}  total_flahes: {}".format(step, step_flashes, total_flashes))

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    data = []
    for line in fileinput.input():
        data.append([int(i) for i in line.rstrip()])

    logging.debug('Initial data: {})'.format(data))

    before = time.time()
    result = parts(data, 100)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

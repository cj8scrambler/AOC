#!/usr/bin/python3

import logging
import sys
import fileinput
import time
import re
import copy
from itertools import combinations 
  

def show(data):
    #logging.debug("show: {}".format(data))
    for z in range(len(data)):
        logging.error ("z=%d" % (z))
        for y in data[z]:
            line = ""
            for x in y:
                line = line + x
            logging.error ("{}".format(line))

def grow(data):
    #logging.debug("grow: {}".format(data))
    newy = len(data[0]) + 2
    newx = len(data[0][0]) + 2
    logging.debug("grow: newy: %d newx: %d" % (newy, newx))
    for z in data:
        for y in z:
            y.insert(0,'.')
            y.append('.')
        z.insert(0, ['.'] * newy)
        z.append(['.'] * newy)
    data.insert(0, [['.'] * newx for i in range(newy)])
    data.append([['.'] * newx for i in range(newy)])
    
    logging.debug("newdata: {}".format(data))

def neighbors(data, x, y, z):

    n=0
    logging.debug("  Find neighbors of: [%d, %d, %d]" % (z, y, x))
    for zr in range(z-1,z+2):
        if (zr < 0) or (zr >= len(data)):
            #logging.debug("Skip invalid z: %d" % (zr))
            continue
        for yr in range(y-1,y+2):
            if (yr < 0) or (yr >= len(data[0])):
                #logging.debug("Skip invalid y: %d" % (yr))
                continue
            for xr in range(x-1,x+2):
                if (xr < 0) or (xr >= len(data[0])):
                    #logging.debug("Skip invalid x: %d" % (xr))
                    continue
                if (xr == x) and (yr == y) and (zr == z):
                    #logging.debug("  skip me: [%d, %d, %d]" % (zr, yr, xr))
                    continue
                if (data[zr][yr][xr] == '#'):
                    logging.debug("    found neighbor: [%d, %d, %d]" % (zr, yr, xr))
                    n += 1

    logging.debug("  [%d, %d, %d] has %d neighbors" % (z, y, x, n))
    return n

def cycle(data):

    logging.debug("Cycle")
    newdata = copy.deepcopy(data)
    logging.debug("  z range: {}".format(range(0, len(data))))
    for z in range(0, len(data)):
        logging.debug("  y range: {}".format(range(0, len(data[z]))))
        for y in range(0, len(data[z])):
            logging.debug("  x range: {}".format(range(0, len(data[z]))))
            for x in range(0, len(data[z])):
                logging.debug("Cycle: on [%d,%d,%d]" % (z, y, x))
                n = neighbors(data, x, y, z)
                if data[z][y][x] == '#':
                    if (n != 2) and (n != 3):
                        newdata[z][y][x] = '.'
                        logging.info("  [%d,%d,%d] # -> %c" % (z, y, x, newdata[z][y][x]))
                else:
                    if (n == 3):
                        newdata[z][y][x] = '#'
                        logging.info("  [%d,%d,%d] . -> %c" % (z, y, x, newdata[z][y][x]))
    return newdata

def count(data):

    sum = 0
    logging.debug("  z range: {}".format(range(0, len(data))))
    for z in range(0, len(data)):
        logging.debug("  y range: {}".format(range(0, len(data[z]))))
        for y in range(0, len(data[z])):
            logging.debug("  x range: {}".format(range(0, len(data[z]))))
            for x in range(0, len(data[z])):
                if data[z][y][x] == '#':
                    sum += 1
    return sum


def part1(data):

    #show(data)
    for each in range(6):
        logging.error("##### Cycle %d ######" % (each +1))
        grow(data)
        newdata = cycle(data)
        #show(newdata)
        data = newdata
        logging.debug("")
    return count(data)


if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)

    # data[z][y][x]
    data = [[]]

    for line in fileinput.input():
        data[0].append(list(line.rstrip()))

    result = part1(data)
    print("Part 1: %d" % result)

    #result = part2(rules, [tickets[0]] + goodlist)
    #print("Part 2: {}".format(result))

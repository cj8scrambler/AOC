#!/usr/bin/python

import logging
import sys
import fileinput
import time
import re
from itertools import combinations 
  
def showme(data):
    for line in data:
        logging.info("  {0}".format(line))

def slope(data, sx, sy):
    width=len(data[0])
    height=len(data)
    logging.debug("x: %d   y: %d" % (width, height))

    x=0
    tree=0
    for y in range(0, height, sy):
        logging.debug("step %d: (%d,%d) %c" % (y+1, x, y, data[y][x]))
        tree += (data[y][x] == '#')
        x = (x+sx) % width

    return tree

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    data = [list(line.rstrip()) for line in fileinput.input()]

    #showme(data);
    print("Problem 1 Trees: %d" % (slope(data, 3, 1)));

    product=1

    sv = slope(data, 1, 1);
    product = sv * product
    print("Problem 2 (1,1) Trees: %d  Total: %d" % (sv, product))

    sv = slope(data, 3, 1);
    product = sv * product
    print("Problem 2 (3,1) Trees: %d  Total: %d" % (sv, product))

    sv = slope(data, 5, 1);
    product = sv * product
    print("Problem 2 (5,1) Trees: %d  Total: %d" % (sv, product))

    sv = slope(data, 7, 1);
    product = sv * product
    print("Problem 2 (7,1) Trees: %d  Total: %d" % (sv, product))

    sv = slope(data, 1, 2);
    product = sv * product
    print("Problem 2 (1,2) Trees: %d  Total: %d" % (sv, product))

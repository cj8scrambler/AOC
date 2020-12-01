#!/usr/bin/python

import logging
import sys
import fileinput
import time
from itertools import combinations 
  
def showme(data):
    for line in data:
        logging.info("  On: {0}".format(line))

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [int(line) for line in fileinput.input()]

    showme(lines)

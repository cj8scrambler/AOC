#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

def part2(data):
  return(0)
  
def part1(data):
  return(0)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [line.strip() for line in fileinput.input()]

    before = time.time()
    result = part1(lines)
    after = time.time()
    print("results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

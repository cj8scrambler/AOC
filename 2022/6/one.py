#!/usr/bin/python

import logging
import sys
import re
import fileinput
import time
from itertools import combinations 

MAX_STACKS=9

def part1(data):

  b = 0
  e = 4
  for i in range(3, len(data)+1):
    print(data[b:e])
    if len(set(data[b:e])) == 4:
        print("found 4 unique at b={}  e={}".format(b,e))
        return e
    b += 1
    e += 1
    
  return(0)

def part2(data):

  b = 0
  e = 14
  for i in range(13, len(data)+1):
    print(data[b:e])
    if len(set(data[b:e])) == 14:
        print("found 14 unique at b={}  e={}".format(b,e))
        return e
    b += 1
    e += 1
    
  return(0)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    lines = [line for line in fileinput.input()]

    before = time.time()
    result = part1(lines[0])
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines[0])
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

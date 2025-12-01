#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 


def part2(data):
  NUMSTRINGS = [ None, "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ]
  total = 0
  for line in data:
    logging.debug("Line: {}".format(line))
    first = None
    last = None

    while (len(line)):
      val = None
      for i, s in  enumerate(NUMSTRINGS):
        if s is not None and line.startswith(s):
          #line = line[len(s):]
          line = line[1:]
          val = i%10
          #logging.debug("  Matched: {} val: {}  now: {}".format(s, val, line))
          if first is None:
            #logging.debug("  Found first num: {}".format(val))
            first = val
          last = val
          break
      if val is None:
        line = line[1:]

    total += int("{}{}".format(first,last))
    logging.debug("  Got: {}{}  total: {}".format(first,last,total))
    
  return(total)
  
def part1(data):
  total = 0
  for line in data:
    logging.debug("Line: {}".format(line))
    first = None
    last = None
    for c in line:
      if c.isnumeric():
        if first is None:
          logging.debug("  Found first num: {}".format(c))
          first = c
        last = c
    if first is not None:
      total += int("{}{}".format(first,last))
      logging.debug("  Got: {}{}  total: {}".format(first,last,total))
   
  return(total)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    lines = [line.strip() for line in fileinput.input()]

    #before = time.time()
    #result = part1(lines)
    #after = time.time()
    #print("results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

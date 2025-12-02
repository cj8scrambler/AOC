#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
import copy
from itertools import combinations 
from collections import defaultdict 

def part2(data):
  zeros = 0
  pos = 50

  for instruction in data:
    dir = instruction[0]
    len = int(instruction[1:])

    if len == 0:
      print(f"Skipping {instruction}")
      continue

    if dir == 'L':
      len = len * -1

    if len > 0:
      if pos + len > 100:
        zeros += (pos + len) // 100
    elif pos != 0:
      if pos + len <= 0:
        zeros += 1 + abs (pos + len) // 100
    elif len <= -100:
      zeros += abs (len) // 100
    pos += len
    pos %= 100

  return(zeros)

def part1(data):
  zeros = 0
  pos = 50

  for instruction in data:
    dir = instruction[0]
    len = int(instruction[1:])

    if dir == 'L':
      len = len * -1

    pos = pos + len
    while (pos < 0):
      pos = pos + 100
    pos = pos % 100

    if pos == 0:
      zeros = zeros + 1

    print(f"{instruction}: {pos} [{zeros}]")

  return(zeros)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [line.strip() for line in fileinput.input()]

#    before = time.time()
#    result = part1(lines)
#    after = time.time()
#    print("part 1 results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

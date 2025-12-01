#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

def blink(data):
  out = []

  for each in data:
    if (each == 0):
      out.append(1)
#      print (f"  {each} is 0: replace with {out[-1]}")
    elif (len(str(each))%2) == 0:
      numlen = int(len(str(each))/2)
      out.append(int(str(each)[0:numlen]))
      out.append(int(str(each)[numlen:]))
#      print (f"  {each} is even # digits: split {out[-2]}, {out[-1]}")
    else:
      out.append(each * 2024)
#      print (f"  {each} is other: scaled to {out[-1]}")
  return out

def part2(data):
  return(0)
  
def part1(data):
  before = time.time()
  new = [int(i) for i in data[0]]
  for i in range(75):
    new = blink(new)
    print(i)
    print("time: {:.1f} min".format((time.time() - before)/60))
  return(len(new))

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [line.strip().split() for line in fileinput.input()]

    before = time.time()
    result = part1(lines)
    after = time.time()
    print("results: {} ({:.3f} sec)".format(result, (after - before)))

#    before = time.time()
#    result = part2(lines)
#    after = time.time()
#    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

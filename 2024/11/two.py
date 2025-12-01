#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

logged_depth = 0
solved = defaultdict(dict)

def blink_stone(stone, num):
  global logged_depth

  if num in solved[stone]:
    #print (" "*(25-num) + f"{stone}: USED SOLVED VALUE: {solved[stone][num]}")
    return solved[stone][num]

  if (num == 0):
    #print (" "*(25-num) + f"{stone}: done: returning 1")
    return 1

  if (stone == 0):
    #print (" "*(25-num) + f"{stone}: flip to 1; num: {num}")
    val = blink_stone(1, num - 1)
    solved[stone][num] = val
    #print (" "*(25-num) + f"{stone}: set solved[{stone}][{num}] = {val}")
    return val

  if (len(str(stone))%2) == 0:
    numlen = int(len(str(stone))/2)
    s1 = int(str(stone)[0:numlen])
    s2 = int(str(stone)[numlen:])
    #print (" "*(25-num) + f"{stone}: split to {s1} and {s2}; num: {num}")
    val1 =  blink_stone(s1, num - 1)
    val2 =  blink_stone(s2, num - 1)
    solved[stone][num] = val1 + val2
    #print (" "*(25-num) + f"{stone}: set solved[{stone}][{num}] = {val1} + {val2}")
    return (val1 + val2)

  #print(" "*(25-num) + f"{stone}: change to {2024*stone}; num: {num}")
  val = blink_stone(stone * 2024, num - 1)
  #print (" "*(25-num) + f"{stone}: children returned {val}")
  solved[stone][num] = val
  #print (" "*(25-num) + f"{stone}: set solved[{stone}][{num}] = {val}")
  return val

def part2(data, num):

  result = 0 

  for stone in [int(i) for i in data[0]]:
    result += blink_stone(stone, num)

  return(result)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [line.strip().split() for line in fileinput.input()]

#    before = time.time()
#    result = part1(lines)
#    after = time.time()
#    print("results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines, 75)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

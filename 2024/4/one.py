#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

def xmas(data, x, y):
  found = 0
  #Check right
  if (x + 3 < len(data[y])):
    if (data[y][x+1] == 'M') and (data[y][x+2] == 'A') and (data[y][x+3] == 'S'):
      print(f"Found right starting at [{x}][{y}]")
      found += 1

  #Check left
  if (x >= 3):
    if (data[y][x-1] == 'M') and (data[y][x-2] == 'A') and (data[y][x-3] == 'S'):
      print(f"Found left starting at [{x}][{y}]")
      found += 1

  #Check down
  if (y + 3 < len(data)):
    if (data[y+1][x] == 'M') and (data[y+2][x] == 'A') and (data[y+3][x] == 'S'):
      print(f"Found down starting at [{x}][{y}]")
      found += 1

  #Check up
  if (y >= 3):
    if (data[y-1][x] == 'M') and (data[y-2][x] == 'A') and (data[y-3][x] == 'S'):
      print(f"Found down starting at [{x}][{y}]")
      found += 1

  #Check up-right
  if (y >= 3) and (x + 3 < len(data[y])):
    if (data[y-1][x+1] == 'M') and (data[y-2][x+2] == 'A') and (data[y-3][x+3] == 'S'):
      print(f"Found up-right starting at [{x}][{y}]")
      found += 1

  #Check down-right
  if (y + 3 < len(data)) and (x + 3 < len(data[y])):
    if (data[y+1][x+1] == 'M') and (data[y+2][x+2] == 'A') and (data[y+3][x+3] == 'S'):
      print(f"Found up-right starting at [{x}][{y}]")
      found += 1

  #Check down-left
  if (y + 3 < len(data)) and (x >= 3):
    if (data[y+1][x-1] == 'M') and (data[y+2][x-2] == 'A') and (data[y+3][x-3] == 'S'):
      print(f"Found up-right starting at [{x}][{y}]")
      found += 1

  #Check up-left
  if (y >= 3) and (x >= 3):
    if (data[y-1][x-1] == 'M') and (data[y-2][x-2] == 'A') and (data[y-3][x-3] == 'S'):
      print(f"Found up-right starting at [{x}][{y}]")
      found += 1

  return found

def crossmas(data, x, y):
  found = 0

  if (y >= 1) and (y + 1 < len(data)) and \
     (x >= 1) and (x + 1 < len(data[y])):

    #Check MS-A-MS
    if (data[y-1][x-1] == 'M') and (data[y-1][x+1] == 'S') and \
       (data[y+1][x-1] == 'M') and (data[y+1][x+1] == 'S'):
      print(f"Found MS-A-MS at [{x}][{y}]")
      found += 1

    #Check MM-A-SS
    if (data[y-1][x-1] == 'M') and (data[y-1][x+1] == 'M') and \
       (data[y+1][x-1] == 'S') and (data[y+1][x+1] == 'S'):
      print(f"Found MM-A-SS at [{x}][{y}]")
      found += 1

    #Check SM-A-SM
    if (data[y-1][x-1] == 'S') and (data[y-1][x+1] == 'M') and \
       (data[y+1][x-1] == 'S') and (data[y+1][x+1] == 'M'):
      print(f"Found SM-A-SM at [{x}][{y}]")
      found += 1

    #Check SS-A-MM
    if (data[y-1][x-1] == 'S') and (data[y-1][x+1] == 'S') and \
       (data[y+1][x-1] == 'M') and (data[y+1][x+1] == 'M'):
      print(f"Found SS-A-MM at [{x}][{y}]")
      found += 1

  return found

def part1(data):
  result = 0
  for y,row in enumerate(data):
    for x,val in enumerate(row):
      if (val == 'X'):
        result += xmas(data, x, y)
  return(result)

def part2(data):
  result = 0
  for y,row in enumerate(data):
    for x,val in enumerate(row):
      if (val == 'A'):
        result += crossmas(data, x, y)
  return(result)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [line.strip() for line in fileinput.input()]

#    before = time.time()
#    result = part1(lines)
#    after = time.time()
#    print("results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

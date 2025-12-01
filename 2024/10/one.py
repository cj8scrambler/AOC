#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

def rating(height, x, y, data):
  result = list()

#  print(f" " * height + f"begin [{x}][{y}]")

  # Down
  if (y + 1 < len(data)) and (int(data[y+1][x]) == height + 1):
    if (height + 1 == 9):
      print(f" " * height + f" found down path to height 9 @ [{x}][{y+1}]")
      result.append((x, y+1))
    else:
      for each in rating(height+1, x, y+1, data):
        result.append(each)

  # Left
#  print(f" " * height + f" check if ({x} > 0) and left neighbor {data[y][x-1]} == {height+1}")
  if (x >= 1) and (int(data[y][x-1]) == height + 1):
    if (height + 1 == 9):
      print(f" " * height + f" found left path to height 9 @ [{x-1}][{y}]")
      result.append((x-1, y))
    else:
#      print(f" " * height + f" matched; going to recurse to [{x-1}][{y}]")
      for each in rating(height+1, x-1, y, data):
        result.append(each)
#  else:
#    print(f" " * height + f" no match")

  # Up
  if (y >= 1) and (int(data[y-1][x]) == height + 1):
    if (height + 1 == 9):
      print(f" " * height + f" found up path to height 9 @ [{x}][{y-1}]")
      result.append((x, y-1))
    else:
      for each in rating(height+1, x, y-1, data):
        result.append(each)

  # Right
  if (x + 1 < len(data[y])) and (int(data[y][x+1]) == height + 1):
    if (height + 1 == 9):
      print(f" " * height + f" found right path to height 9 @ [{x+1}][{y}]")
      result.append((x+1, y))
    else:
      for each in rating(height+1, x+1, y, data):
        result.append(each)

  return result

def follow(height, x, y, data):
  result = set()

#  print(f" " * height + f"begin [{x}][{y}]")

  # Down
  if (y + 1 < len(data)) and (int(data[y+1][x]) == height + 1):
    if (height + 1 == 9):
      print(f" " * height + f" found path to height 9 @ [{x}][{y+1}]")
      result.add((x, y+1))
    else:
      for each in follow(height+1, x, y+1, data):
        result.add(each)

  # Left
#  print(f" " * height + f" check if ({x} > 0) and left neighbor {data[y][x-1]} == {height+1}")
  if (x >= 1) and (int(data[y][x-1]) == height + 1):
    if (height + 1 == 9):
      print(f" " * height + f" found path to height 9 @ [{x-1}][{y}]")
      result.add((x-1, y))
    else:
#      print(f" " * height + f" matched; going to recurse to [{x-1}][{y}]")
      for each in follow(height+1, x-1, y, data):
        result.add(each)
#  else:
#    print(f" " * height + f" no match")

  # Up
  if (y >= 1) and (int(data[y-1][x]) == height + 1):
    if (height + 1 == 9):
      print(f" " * height + f" found path to height 9 @ [{x}][{y-1}]")
      result.add((x, y-1))
    else:
      for each in follow(height+1, x, y-1, data):
        result.add(each)

  # Right
  if (x + 1 < len(data[y])) and (int(data[y][x+1]) == height + 1):
    if (height + 1 == 9):
      print(f" " * height + f" found path to height 9 @ [{x+1}][{y}]")
      result.add((x+1, y))
    else:
      for each in follow(height+1, x+1, y, data):
        result.add(each)

  return result

def numpaths(x, y, data):
  result = follow(0, x, y, data)

  print(f"[{x}][{y}] returned: {len(result)}")
  return len(result)

def rate(x, y, data):
  result = rating(0, x, y, data)

  print(f"[{x}][{y}] returned: {len(result)}")
  return len(result)


def part1(data):
  result = 0
  for y,row in enumerate(data):
    for x,val in enumerate(row):
      if (val == '0'):
        result += numpaths(x, y, data)
  return(result)

def part2(data):
  result = 0
  for y,row in enumerate(data):
    for x,val in enumerate(row):
      if (val == '0'):
        result += rate(x, y, data)
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

#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

rotate_map = {
  '^': '>',
  '>': 'v',
  'v': '<',
  '<': '^',
}

def printmap(data):
  for row in data:
    for val in row:
      print(val, end="")
    print("")

def in_bounds(pos, data):

  if (pos[0] < 0) or (pos[0] >= len(data[0])) or \
     (pos[1] < 0) or (pos[1] >= len(data)):
    #print(f"Position {pos} is out of bounds")
    return False
  return True

def step(pos, data):

  new_pos = (None, None)

  if data[pos[1]][pos[0]] == '^':
    new_pos = (pos[0], pos[1]-1)
    #print(f"move up to {new_pos}")
  elif data[pos[1]][pos[0]] == '>':
    new_pos = (pos[0]+1, pos[1])
    #print(f"move right to {new_pos}")
  elif data[pos[1]][pos[0]] == 'v':
    new_pos = (pos[0], pos[1]+1)
    #print(f"move down to {new_pos}")
  elif data[pos[1]][pos[0]] == '<':
    new_pos = (pos[0]-1, pos[1])
    #print(f"move left to {new_pos}")
  else: 
    print(f"Error: {pos} has unkown direction: {data[pos[1]][pos[0]]}")

  if not in_bounds(new_pos, data):
    data[pos[1]][pos[0]] = 'X'
    print(f"Moved to INVALID new pos: {new_pos}: return None")
    return None
  elif (data[new_pos[1]][new_pos[0]] == '.') or (data[new_pos[1]][new_pos[0]] == 'X'):
    data[new_pos[1]][new_pos[0]] = data[pos[1]][pos[0]]
    data[pos[1]][pos[0]] = 'X'
    #print(f"Moved to {new_pos}: {data[new_pos[1]][new_pos[0]]}")
    return new_pos
  elif (data[new_pos[1]][new_pos[0]] == '#'):
    # turn 90
    data[pos[1]][pos[0]] = rotate_map[data[pos[1]][pos[0]]]
    #print(f"Rotate at {pos} to {data[pos[1]][pos[0]]}")
    return pos
  raise Exception("Invalid new posistion value at {new_pos}: data[new_pos[1]][new_pos[0]")

def part1(data):
  result = 0
  pos = (None, None)

  #find starting point
  for y,row in enumerate(data):
    for x,value in enumerate(row):
      if value == '^':
        pos = (x, y)

  print(f"Starting point: {pos}");

  while pos != None:
    pos = step(pos, data)
    #printmap(data)
    print("")

  # Cound the Xs
  for row in data:
    result += row.count('X')

  print(f"Traveled {result} unique points")

  return(result)

def part2(data):
  result = 0
  return(result)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [list(line.strip()) for line in fileinput.input()]

    before = time.time()
    result = part1(lines)
    after = time.time()
    print("results: {} ({:.3f} sec)".format(result, (after - before)))

#    before = time.time()
#    result = part2(lines)
#    after = time.time()
#    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

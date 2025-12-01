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

rotate_map = {
  '^': '>',
  '>': 'v',
  'v': '<',
  '<': '^',
}

history_map = {
  '^': 'U',
  '>': 'R',
  'v': 'D',
  '<': 'L',
}

def printmap(data):
  for row in data:
    for val in row:
      if (val[-1] == '.') or (val[-1] == '#') or (val[-1] in history_map):
        print(val[-1], end="")
      else:
        print(val[-1], end="")
    print("")

def in_bounds(pos, data):

  if (pos[0] < 0) or (pos[0] >= len(data[0])) or \
     (pos[1] < 0) or (pos[1] >= len(data)):
    #print(f"Position {pos} is out of bounds")
    return False
  return True

def detect_loop(pos, new_pos, data):

#  if (data[pos[1]][pos[0]][-1] == '^'):
#    print(f"Check for 'U' in {new_pos} history: {data[new_pos[1]][new_pos[0]]}")
  if (data[pos[1]][pos[0]][-1] == '^') and ('U' in data[new_pos[1]][new_pos[0]]):
#    print(f"  Loop detected at {pos} -> {new_pos}")
    return True

#  if (data[pos[1]][pos[0]][-1] == '>'):
#    print(f"Check for 'R' in {new_pos} history: {data[new_pos[1]][new_pos[0]]}")
  if (data[pos[1]][pos[0]][-1] == '>') and ('R' in data[new_pos[1]][new_pos[0]]):
#    print(f"  Loop detected at {pos} -> {new_pos}")
    return True

#  if (data[pos[1]][pos[0]][-1] == 'v'):
#    print(f"Check for 'D' in {new_pos} history: {data[new_pos[1]][new_pos[0]]}")
  if (data[pos[1]][pos[0]][-1] == 'v') and ('D' in data[new_pos[1]][new_pos[0]]):
#    print(f"  Loop detected at {pos} -> {new_pos}")
    return True

#  if (data[pos[1]][pos[0]][-1] == '<'):
#    print(f"Check for 'L' in {new_pos} history: {data[new_pos[1]][new_pos[0]]}")
  if (data[pos[1]][pos[0]][-1] == '<') and ('L' in data[new_pos[1]][new_pos[0]]):
#    print(f"  Loop detected at {pos} -> {new_pos}")
    return True

  return False

def step(pos, data):

  new_pos = (None, None)

  if data[pos[1]][pos[0]][-1] == '^':
    new_pos = (pos[0], pos[1]-1)
    #print(f"move up to {new_pos}")
  elif data[pos[1]][pos[0]][-1] == '>':
    new_pos = (pos[0]+1, pos[1])
    #print(f"move right to {new_pos}")
  elif data[pos[1]][pos[0]][-1] == 'v':
    new_pos = (pos[0], pos[1]+1)
    #print(f"move down to {new_pos}")
  elif data[pos[1]][pos[0]][-1] == '<':
    new_pos = (pos[0]-1, pos[1])
    #print(f"move left to {new_pos}")
  else: 
    print(f"Error: {pos} has unkown direction: {data[pos[1]][pos[0]][-1]}")

  if not in_bounds(new_pos, data):
    data[pos[1]][pos[0]].append(history_map[data[pos[1]][pos[0]][-1]])
    #print(f"Done detected at new pos: {new_pos}: return DONE")
    return 'DONE'
  else:
    if detect_loop(pos, new_pos, data):
      #print(f"Loop Detected at new pos: {new_pos}: {data[new_pos[1]][new_pos[0]][-1]}")
      return 'LOOP'
    elif (data[new_pos[1]][new_pos[0]][-1] == '.') or (data[new_pos[1]][new_pos[0]][-1] == 'X') or \
         (data[new_pos[1]][new_pos[0]][-1] == 'U') or (data[new_pos[1]][new_pos[0]][-1] == 'R') or \
         (data[new_pos[1]][new_pos[0]][-1] == 'D') or (data[new_pos[1]][new_pos[0]][-1] == 'L') :
      data[new_pos[1]][new_pos[0]].append(data[pos[1]][pos[0]][-1])
      data[pos[1]][pos[0]].append(history_map[data[new_pos[1]][new_pos[0]][-1]])
      #print(f"Moved to {new_pos}: {data[new_pos[1]][new_pos[0]][-1]}")
      return new_pos
    elif (data[new_pos[1]][new_pos[0]][-1] == '#'):
      direction = data[pos[1]][pos[0]][-1]
      #save the incoming direction history
      data[pos[1]][pos[0]].append(history_map[direction])
      # turn 90
      data[pos[1]][pos[0]].append(rotate_map[direction])
      #print(f"Rotate at {pos} to {data[pos[1]][pos[0]][-1]}")
      return pos
    raise Exception("Invalid new posistion value at {new_pos}: data[new_pos[1]][new_pos[0]")

def part2(data):
  result = 0
  start_pos = 'EMPTY'

  #find starting point and convert every value to a list
  for y,row in enumerate(data):
    for x,value in enumerate(row):
      if value == '^':
        start_pos = (x, y)
      data[y][x] = [value]


  print(f"Starting point: {start_pos}");

  for x in list(range(len(data[0]))):
    for y in list(range(len(data))):
      print(f"Try with obstacle at {(x,y)} ({round(100*x/len(data[0]))} % done)")
      if (x, y) != start_pos:
        trydata = copy.deepcopy(data)
        trydata[y][x] = ['#']
        pos = start_pos
        while pos != 'LOOP' and pos != 'DONE':
          pos = step(pos, trydata)
          #printmap(trydata)
          #print("")
        if pos == 'LOOP':
          print(f"Loop detected with obstacle at {(x,y)}")
          result += 1

  print(f"Found {result} loop maps")

  return(result)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [list(line.strip()) for line in fileinput.input()]

#    before = time.time()
#    result = part1(lines)
#    after = time.time()
#    print("results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

def printmap(data):
  for y,row in enumerate(data):
    for x,val in enumerate(row):
      print(val, end="")
    print("")

def valid(point, data):
  if (point[0] >= 0) and (point[0] < len(data[0])) and \
     (point[1] >= 0) and (point[1] < len(data)):
    return True
  return False

def robot_loc(data):
  x = None
  y = None
  for y,row in enumerate(data):
    try:
      x = row.index('@')
      break;
    except ValueError:
      continue
  return (x,y)


def eval_dir(point, direction):
  if (direction == '^'):
    return ((point[0], point[1] - 1))
  elif (direction == '>'):
    return ((point[0] + 1, point[1]))
  elif (direction == 'v'):
    return((point[0], point[1] + 1))
  elif (direction == '<'):
    return((point[0] - 1, point[1]))
  return None

def push_box(box, direction, data):
  #print(f"Push box {direction}")
  new = eval_dir(box, direction)
  new_val = data[new[1]][new[0]]

  if new_val == '.':
    #print(f"push box to {new} is open; set {data[new[1]][new[0]]} to 'O'")
    data[new[1]][new[0]] = 'O'
    return True
  elif new_val == '#':
    #print(f"push box to {new} hit wall: done")
    return False
  else:
    if push_box(new, direction, data):
      #print(f"push box to {new} succeeded so update {box} from {data[box[1]][box[0]]} to '.' and {data[new[1]][new[0]]} to 'O'")
      data[new[1]][new[0]] = 'O'
      data[box[1]][box[0]] = '.'
      return True
    else:
      #print(f"push box to {new} failed")
      return False
      
def move(direction, data):
  robot = robot_loc(data)
  new = eval_dir(robot, direction)
  new_val = data[new[1]][new[0]]

  if new_val == '.':
    #print(f"Move {direction}: new_point {new} is free; move there")
    data[robot[1]][robot[0]] = '.'
    data[new[1]][new[0]] = '@'
  #elif new_val == '#':
    #print(f"Move {direction}: new_point {new} is wall; nothing to do")
  elif new_val == 'O':
    #print(f"Move {direction}: new_point {new} has box")
    if (push_box(new, direction, data)):
      data[robot[1]][robot[0]] = '.'
      data[new[1]][new[0]] = '@'

def part1(room, moves):
  result = 0

  print(f"Begin:")
  printmap(room)
  print(f"")

  for m in moves:
    move(m, room)

  print(f"End:")
  printmap(room)
  print(f"")

  for y,row in enumerate(room):
    for x,val in enumerate(row):
      if room[y][x] == 'O':
        result += 100  * y + x
        #print(f"  box at {(x,y)}: add {100*y+x}: {result}")
    
  return(result)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    room = list()
    moves = list()

    for l in [line.strip() for line in fileinput.input()]:
      if len(l) == 0:
        continue
      elif l[0] == '#':
        room.append(list(l));
      else:
        moves += l

    before = time.time()
    result = part1(room, moves)
    after = time.time()
    print("results: {} ({:.3f} sec)".format(result, (after - before)))

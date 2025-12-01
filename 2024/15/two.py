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


def push_box(box_l, box_r, direction, data):
  print(f"Push box {box_l}/{box_r}: {direction}")
  new_l = eval_dir(box_l, direction)
  new_l_val = data[new_l[1]][new_l[0]]
  new_r = eval_dir(box_r, direction)
  new_r_val = data[new_r[1]][new_r[0]]

  if direction == '<':
    if new_l_val == '.':
      print(f"  push box left to {new_l}/{new_r} is open; move box there")
      data[new_l[1]][new_l[0]] = '['
      data[new_r[1]][new_r[0]] = ']'
      printmap(data)
      return True
    elif new_l_val == '#'
      print(f"  push box left to {new} hit wall: done")
      return False
    elif push_box(new_l, new_r, direction, data):
      print(f"  push box to left {new_l}/{new_r} succeeded so update ")
      #data[box_l[1]][box_l[0]] = '.'
      data[box_r[1]][box_r[0]] = '.'
      data[new_r[1]][new_r[0]] = ']'
      data[new_l[1]][new_l[0]] = '['
      printmap(data)
      return True
    else:
      print(f"  push box to {new} failed")
      return False
  elif direction == '>':
    if new_r_val == '.':
      print(f"  push box right to {new_l}/{new_r} is open; move box there")
      data[new_l[1]][new_l[0]] = '['
      data[new_r[1]][new_r[0]] = ']'
      printmap(data)
      return True
    elif new_r_val == '#'
      print(f"  push box right to {new} hit wall: done")
      return False
    elif push_box(new_l, new_r, direction, data):
      print(f"  push box to right {new_l}/{new_r} succeeded so update ")
      data[box_l[1]][box_l[0]] = '.'
      #data[box_r[1]][box_r[0]] = '.'
      data[new_l[1]][new_l[0]] = '['
      data[new_r[1]][new_r[0]] = ']'
      printmap(data)
      return True
    else:
      print(f"  push box to {new} failed")
      return False
  # Up/Down
  else:
    if new_l_val == '.' and new_r_val == '.':
      print(f"  push box to {new_l}/{new_r} is open; move box there")
      data[new_l[1]][new_l[0]] = '['
      data[new_r[1]][new_r[0]] = ']'
      printmap(data)
      return True
    elif new_l_val == '#' or new_r_val == '#':
      print(f"  push box to {new} hit wall: done")
      return False
    # Directly under/over another box
    elif new_l_val == '[' and new_r_val == ']':
      if push_box(new_l, new_r, direction, data):
        print(f"  push box to {new_l}/{new_r} succeeded so update ")
        data[box_l[1]][box_l[0]] = '.'
        data[box_r[1]][box_r[0]] = '.'
        data[new_l[1]][new_l[0]] = '['
        data[new_r[1]][new_r[0]] = ']'
        printmap(data)
        return True
      else:
        print(f"  push box to {new} failed")
        return False
    # Offset under/over another box
    else:
#      # Offset left under/over another box
#      if new_l_val == ']':
#      if push_box(new_l, new_r, direction, data):
#        print(f"  push box to {new_l}/{new_r} succeeded so update ")
#        data[box_l[1]][box_l[0]] = '.'
#        data[box_r[1]][box_r[0]] = '.'
#        data[new_l[1]][new_l[0]] = '['
#        data[new_r[1]][new_r[0]] = ']'
#        printmap(data)
#        return True
#      else:
#        print(f"  push box to {new} failed")
#        return False
      
def move(direction, data):
  robot = robot_loc(data)
  new = eval_dir(robot, direction)
  new_val = data[new[1]][new[0]]

  if new_val == '.':
    print(f"Move {direction}: new_point {new} is free; move there")
    data[robot[1]][robot[0]] = '.'
    data[new[1]][new[0]] = '@'
  elif new_val == '#':
    print(f"Move {direction}: new_point {new} is wall; nothing to do")
  elif new_val == '[':
    print(f"Move {direction}: new_point {new} has left side of box")
    if (push_box(new, (new[0]+1, new[1]), direction, data)):
      data[robot[1]][robot[0]] = '.'
      data[new[1]][new[0]] = '@'
  elif new_val == ']':
    print(f"Move {direction}: new_point {new} has right side of box")
    if (push_box((new[0]-1, new[1]), new, direction, data)):
      data[robot[1]][robot[0]] = '.'
      data[new[1]][new[0]] = '@'

def part2(room, moves):
  result = 0

  print(f"Begin:")
  printmap(room)
  print(f"")

  for m in moves:
    move(m, room)
    printmap(room)
    print(f"")

  print(f"End:")
  printmap(room)
  print(f"")

#  for y,row in enumerate(room):
#    for x,val in enumerate(row):
#      if room[y][x] == 'O':
#        result += 100  * y + x
#        #print(f"  box at {(x,y)}: add {100*y+x}: {result}")
    
  return(result)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    room = list()
    moves = list()

    for l in [line.strip() for line in fileinput.input()]:
      if len(l) == 0:
        continue
      elif l[0] == '#':
        room.append([])
        for c in list(l):
          if c == '#':
            room[-1] += ['#', '#']
          elif c == 'O':
            room[-1] += ['[', ']']
          elif c == '.':
            room[-1] += ['.', '.']
          elif c == '@':
            room[-1] += ['@', '.']
      else:
        moves += l

    before = time.time()
    result = part2(room, moves)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

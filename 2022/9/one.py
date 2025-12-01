#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 

def print_grid(size, knots):
  print('print_grid(size={}, knots={}'.format(size, knots))
  for y in reversed(range(size)):
    for x in range(size):
      if ([x,y] in knots):
        mark = str(knots.index([x,y]))
        if mark == '0':
          mark='H'
        print('{}'.format(mark), end="")
      elif ((x,y) in knots):
        print('#', end="")
      else:
        print('.',end="")
    print('');
  print('');

def update_tail(head, tail):
  new_tail = tail[:]  #copy it
 
  if (abs(head[0] - tail[0]) > 1) or \
     (abs(head[1] - tail[1]) > 1):
    
    logging.debug("  upd_tail() going to move");
    if (head[0] > tail[0]):
      logging.debug("  upd_tail() head is right of tail; move tail right");
      new_tail[0] += 1
    elif (head[0] < tail[0]):
      logging.debug("  upd_tail() head is left of tail; move tail left");
      new_tail[0] -= 1

    if (head[1] > tail[1]):
      logging.debug("  upd_tail() head is above tail; move tail up");
      new_tail[1] += 1
    elif (head[1] < tail[1]):
      logging.debug("  upd_tail() head is below tail; move tail down");
      new_tail[1] -= 1

  logging.debug("  upd_tail(h={}, t={}): new tail={}".format(head, tail, new_tail))
  return new_tail
  
def part1(data):

  head = tail = [0,0]
  tail_locs = set()

  for line in data:
    [dir,num] = line.split()
    for i in range(int(num)):
      logging.debug("step: {}".format(dir))
      if dir == 'U':
        head = [head[0], head[1]+1]
      elif dir == 'D':
        head = [head[0], head[1]-1]
      elif dir == 'R':
        head = [head[0]+1, head[1]]
      elif dir == 'L':
        head = [head[0]-1, head[1]]
      else:
        raise("Invalid direction: {}".format(dir))
      logging.debug("  head: {}".format(head))
      tail = update_tail(head, tail)
      tail_locs.add(tuple(tail))
      logging.debug("  tail: {}".format(tail))


  print("All {} tail locations: {}".format(len(tail_locs), tail_locs))
  return(len(tail_locs))

def part2(data):

#  knots = [ [0,0] for i in range(10) ]
  knots = [ [11,5] for i in range(10) ]
  tail_locs = set()

  for line in data:
    [dir,num] = line.split()
    for i in range(int(num)):
      logging.debug("step: {}".format(dir))
      if dir == 'U':
        knots[0] = [knots[0][0], knots[0][1]+1]
      elif dir == 'D':
        knots[0] = [knots[0][0], knots[0][1]-1]
      elif dir == 'R':
        knots[0] = [knots[0][0]+1, knots[0][1]]
      elif dir == 'L':
        knots[0] = [knots[0][0]-1, knots[0][1]]
      else:
        raise("Invalid direction: {}".format(dir))
      logging.debug("  head: {}".format(knots[0]))
      for k in range(1,10):
        knots[k] = update_tail(knots[k-1], knots[k])
        logging.debug("  knot-{}: {}".format(k, knots[k]))
      tail_locs.add(tuple(knots[9]))
      #print_grid(27, knots)

  #print_grid(27, list(tail_locs))
  print("All {} tail locations: {}".format(len(tail_locs), tail_locs))
  return(len(tail_locs))

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

#!/usr/bin/python3

import logging
import copy
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict as dd

MAX_VISITS=1

def part2(data):
  pass

def traverse(elmap, start, distance, end, best):
  (y,x) = start

  el = copy.deepcopy(elmap)
  el[y][x] = 99999

  if start == end:
    logging.debug("{} Found the end at {}".format(' '*distance, start))
    return distance

  left = right = up = down = 999999

  #Left
  if (x > 0) and (el[y][x-1] <= elmap[y][x] + 1):
    if (distance + 1) < best:
      logging.debug("{} Trying left ({})".format(' '*distance, el[y][x-1]))
      left = traverse(el, (y,x-1), distance + 1, end, best)
      logging.debug("{} Left returned: {}".format(' '*distance, left))
      if left < best:
        best = left
    else:
      logging.debug("{} Giving up on left branch ({})".format(' '*distance, distance+1))

  #Right
  if (x < len(el[y])-1) and (el[y][x+1] <= elmap[y][x] + 1):
    if (distance + 1) < best:
      logging.debug("{} Trying right".format(' '*distance))
      right = traverse(el, (y,x+1), distance + 1, end, best)
      logging.debug("{} right returned: {}".format(' '*distance, right))
      if right < best:
        best = right
    else:
      logging.debug("{} Giving up on right branch ({})".format(' '*distance, distance+1))

  #Up
  if (y > 0) and (el[y-1][x] <= elmap[y][x] + 1):
    if (distance + 1) < best:
      logging.debug("{} Trying up".format(' '*distance))
      up = traverse(el, (y-1,x), distance + 1, end, best)
      logging.debug("{} Up returned: {}".format(' '*distance, up))
      if up < best:
        best = up
    else:
      logging.debug("{} Giving up on up branch ({})".format(' '*distance, distance+1))

  #Down
  if (y < len(el)-1) and (el[y+1][x] <= elmap[y][x] + 1):
    if (distance + 1) < best:
      logging.debug("{} Trying down".format(' '*distance))
      down = traverse(el, (y+1,x), distance + 1, end, best)
      logging.debug("{} Down returned: {}".format(' '*distance, down))
      if down < best:
        best = down
    else:
      logging.debug("{} Giving up on up branch ({})".format(' '*distance, distance+1))
    
  if (distance % 8) == 0:
    logging.info("{} Best result was: {}".format(' '*distance, min([left,right,up,down])))

  return(min([left, right, up, down]))

def part1(data):

  result = 0
  el = []
  visited = []

  for y,line in enumerate(data):
    el.append(['?' for x in range(len(line))])
    visited.append(['?' for x in range(len(line))])
    for x,c in enumerate(line):
      if c == 'S':
        start = (y,x)
        el[y][x] = ord('a') - ord('a')
      elif c == 'E':
        end = (y,x)
        el[y][x] = ord('z') - ord('a')
      else:
        el[y][x] = ord(c) - ord('a')
      visited[y][x] = 0
  logging.debug("Start: {}  End: {}  Map:".format(start, end))     
  logging.debug(el)

  result = traverse(el, start, 0, end, 99999)

  return(result)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [line.strip() for line in fileinput.input()]

    before = time.time()
    result = part1(lines)
    after = time.time()
    print("results: {} ({:.3f} sec)".format(result, (after - before)))

#    before = time.time()
#    result = part2(lines)
#    after = time.time()
#    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

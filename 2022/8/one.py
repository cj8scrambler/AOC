#!/usr/bin/python

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 

def treescore(treemap, y, x):

  tree = treemap[y][x]
  left = right = up = down = 0

  # score to left
  for i in reversed(treemap[y][0:x]):
    left += 1
    if tree <= i:
      break;
  logging.debug("[{},{}] {}: left score: {}".format(y,x,tree,left))

  # score to right
  if x < len(treemap[y]) - 1:
    for i in treemap[y][(x+1):len(treemap[y])+1]:
      right += 1
      if tree <= i:
        break;
  logging.debug("[{},{}] {}: right score: {}".format(y,x,tree,right))

  # score to top
  col = [row[x] for row in treemap[0:y]]
  for i in reversed(col):
    up += 1
    if tree <= i:
      break;
  logging.debug("[{},{}] {}: up score: {}".format(y,x,tree,up))

  # score to bottom
  if y < len(treemap) - 1:
    col = [row[x] for row in treemap[y+1:len(treemap)]]
    logging.debug("  down data is: {}".format(col))
    for i in col:
      down += 1
      logging.debug("  down ({}) new down score: {}; continue if  {} > {}".format(i,down, tree, i))
      if tree <= i:
        break;
  logging.debug("[{},{}] {}: down score: {}".format(y,x,tree,down))

  logging.debug("  returning score: {}".format(up*left*right*down))
  logging.debug("")
  return (up*left*right*down)

def is_visible(treemap, y, x):
  tree = treemap[y][x]

  #edges
  if (y == 0) or (y == len(treemap)-1):
    logging.debug("[{},{}] {}: edge - true".format(y,x, tree))
    return True
  if (x == 0) or (x == len(treemap[0])-1):
    logging.debug("[{},{}] {}: edge - true".format(y,x, tree))
    return True

  # Visible from left
  if (tree > max(treemap[y][0:x])):
    logging.debug("[{},{}] {}: left - true".format(y,x, tree))
    return True

  # Visible from right
  if (tree > max(treemap[y][(x+1):len(treemap[y])+1])):
    logging.debug("[{},{}] {}: right - true".format(y,x, tree))
    return True

  # Visible from top
  col = [row[x] for row in treemap[0:y]]
  #logging.debug("[{},{}] {}: check above values: {}".format(y,x,tree,col))
  if (tree > max(col)):
    logging.debug("[{},{}] {}: above - true".format(y,x, tree))
    return True

  # Visible from below
  col = [row[x] for row in treemap[y+1:len(treemap)]]
  #logging.debug("[{},{}] {}: check below values: {}".format(y,x,tree,col))
  if (tree > max(col)):
    logging.debug("[{},{}] {}: below - true".format(y,x, tree))
    return True

  logging.debug("[{},{}] {}: none - false".format(y,x, tree))

def part1(data):

  treemap=[]
  for y,line in enumerate(data):
    treemap.append([])
    for t in line:
      treemap[y].append([int(t)])

  print(treemap)

  part1 = 0
  for y,line in enumerate(treemap):
    for x,val in enumerate(treemap[y]):
      if is_visible(treemap, y, x):
        part1 += 1

  part2 = 0
  for y,line in enumerate(treemap):
    for x,val in enumerate(treemap[y]):
      score = treescore(treemap, y, x)
      if score > part2:
        part2=score 
        logging.info("Part2, new best found at [{},{}] ({}): {}".format(y,x,treemap[y][x], score))

  return(part1, part2)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [line.strip() for line in fileinput.input()]

    before = time.time()
    result = part1(lines)
    after = time.time()
    print("results: {} ({:.3f} sec)".format(result, (after - before)))

#    before = time.time()
#    result = part2(lines[0])
#    after = time.time()
#    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

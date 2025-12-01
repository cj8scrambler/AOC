#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

class KeyMap(dict):
  def __missing__(self, key):
    return key

def part2(data):
  return(0)
  
def part1(data):
  mapdata = {}
  source = dest = None
  for l in lines:
    if ':' in l:
      t = l.split(':')[0]
      if t == "seeds":
        seeds = l.split(':')[1]
        logging.debug("Seeds {}".format(seeds))
      else:
        g = re.match( r"([a-z]+)-to-([a-z]+) map", l)
        if g:
          source = g.group(1)
          dest = g.group(2)
          mapdata[source] = {'dest': dest, 'map': KeyMap()}
          logging.debug("New Map {} -> {}".format(source,dest))
    elif (len(l)):
      d, s, num = map(int, l.split())
      for i in range(num):
        logging.debug("{}->{} map {} -> {}".format(source, dest, s+i, d+i))
        mapdata[source]['map'][s+i] = d+i

  for seed in seeds:
    dtype = mapdata['seed']['dest']
    dval = mapdata['seed']['map'][seed]
    while dtype != 'location':
      target = mapdata

  return(0)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    lines = [line.strip() for line in fileinput.input()]

    before = time.time()
    result = part1(lines)
    after = time.time()
    print("results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

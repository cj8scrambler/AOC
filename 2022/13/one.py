#!/usr/bin/python3

import logging
import ast
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


def validate(pair):
  for pos in range(min(len(pair['left']), len(pair['right']))):
    ltype = type(pair['left'][pos])
    rtype = type(pair['right'][pos])
    logging.debug(f"Pair-{i}:[{pos}]:  {p['left'][pos]}({type(p['left'][pos])})  {p['right'][pos]}({type(p['right'][pos])})")
    if (ltype == int) and (rtype == int):
      if pair['left'] < pair['right']
        logging.debug(f"Pair-{i}:[{pos}]: INTS: return True")
        return True
      elif pair['left'] > pair['right']
        logging.debug(f"Pair-{i}:[{pos}]: INTS: return False")
        return False
    elif (ltype == list) and (rtype == list):
      return validate( {'left'}: :q


def part1(data):

  packets = []
  result = 0

  side = ['left', 'right', None]
  pair={'left':None, 'right':None}
  for y,line in enumerate(data):
    position = side[y%3]
    if position:
      pair[position] = ast.literal_eval(line)
      if position == 'right':
        packets.append(pair)
    else:
      pair={'left':None, 'right':None}

  for i,p in enumerate(packets):
    logging.debug(f"Pair-{i}:  {p}")
    for pos in range(min(len(p['left']), len(p['right']))):
      ltype = type(p['left'][pos])
      rtype = type(p['left'][pos])
      if (ltype == int) and (rtype == int):
        
    logging.debug("")

  return(result)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    lines = [line.strip() for line in fileinput.input()]

    before = time.time()
    result = part1(lines)
    after = time.time()
    print("results: {} ({:.3f} sec)".format(result, (after - before)))

#    before = time.time()
#    result = part2(lines)
#    after = time.time()
#    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

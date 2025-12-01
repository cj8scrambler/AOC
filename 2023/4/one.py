#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from collections import defaultdict 
from itertools import combinations 

def part2(data):
  result = 0
  extras = defaultdict(lambda: 1) 
  for line,l in enumerate(data):
    card = line+1
    matches = 0;
    winners,mine = l.split(':')[1].split('|')
    m = mine.split()
    for w in winners.split():
      if w in m:
        matches += 1
    logging.debug("card-{} has {} matches x {} copies".format(card, matches, extras[card]))
    if matches:
      for c in range(card+1, card+1+matches):
        logging.debug("  card-{} increment from {} to {}".format(c, extras[c], extras[c]+extras[card]))
        extras[c] += extras[card]

  for c in extras.values():
    result += c
    
  logging.debug(result)
  return(result)
  
def part1(data):
  result = 0
  for game,l in enumerate(data):
    matches = 0;
    winners,mine = l.split(':')[1].split('|')
    m = mine.split()
    for w in winners.split():
      if w in m:
        matches += 1
    if matches > 0: 
      result += pow(2,matches-1)
  return(result)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    lines = [line.strip() for line in fileinput.input()]

    #before = time.time()
    #result = part1(lines)
    #after = time.time()
    #print("results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

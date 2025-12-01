#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

def part2(data):
  return(0)
  
def part1(rules, updates):
  result = 0
  orders = defaultdict(list)

  for r in rules:
    orders[r[0]].append(r[1])

  for update in updates:
    #print(f"On Update: {update}")
    valid = True
    for page in update:
      #print(f"  on page-{page}")
      if page in orders:
        for rule in orders[page]:
          if rule in update:
            if (update.index(page) >= update.index(rule)):
              valid = False
              #print(f"   ERROR: {page} is NOT before {rule}")
            #else:
              #print(f"   {page} is before {rule}")
          #else:
            #print(f"   {rule} is not in this set")
    if valid: 
      result += int(update[int((len(update)-1)/2)])
      print(f"Update {update} is valid; middle index is {int((len(update)-1)/2)}: {update[int((len(update)-1)/2)]}  result: {result}")
      
  return(result)

if __name__ == '__main__':

  logging.basicConfig(level=logging.INFO)
  rules = []
  updates = []

  for line in [line.strip() for line in fileinput.input()]:
    if '|' in line:
      rules.append(line.split('|'))
    if ',' in line:
      updates.append(line.split(','))

  before = time.time()
  result = part1(rules, updates)
  after = time.time()
  print("results: {} ({:.3f} sec)".format(result, (after - before)))

#  before = time.time()
#  result = part2(lines)
#  after = time.time()
#  print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

def part2(rules, updates):
  result = 0
  orders = defaultdict(list)

  for r in rules:
    orders[r[0]].append(r[1])

  for update in updates:
    print(f"On Update: {update}")
    modified = False
    for page in update:
      print(f"  on page-{page}")
      if page in orders:
        for rule in orders[page]:
          if rule in update:
            if (update.index(page) >= update.index(rule)):
              modified = True
#              print(f"   ERROR: {page} is NOT before {rule}")
              update.remove(page)
              update.insert(update.index(rule), page)
              print(f"   MOVED: {page} to before {rule}: {update}")
            else:
              print(f"   {page} is before {rule}")
          else:
            print(f"   {rule} is not in this set")
    if modified:
      result += int(update[int((len(update)-1)/2)])
      print(f"Update {update} was fixed; middle index is {int((len(update)-1)/2)}: {update[int((len(update)-1)/2)]}  result: {result}")
      
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

#  before = time.time()
#  result = part1(rules, updates)
#  after = time.time()
#  print("results: {} ({:.3f} sec)".format(result, (after - before)))

  before = time.time()
  result = part2(rules, updates)
  after = time.time()
  print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

def part1(data):
  list1 = []
  list2 = []
  total = 0

  for each in data:
    list1.append(int(each[0]))
    list2.append(int(each[1]))
  list1.sort()
  list2.sort()
  for i,v in enumerate(list1):
    distance = abs(list1[i] - list2[i])
    total += distance
    print(f"{list1[i]} -> {list2[i]} = {distance}")
  return(total)

def part2(data):
  list1 = []
  list2 = []
  total = 0

  for each in data:
    list1.append(int(each[0]))
    list2.append(int(each[1]))
  list1.sort()
  list2.sort()

  j = 0
  last_j = 0
  max_j = len(list2)
  for i,x in enumerate(list1):
    match_count = 0
    last_j = j
    #print (f"look for list1[{i}]: {x} starting at list2[{j}]")
    if x in list2 and j < max_j:
      #print (f"  it's possible")
      while list2[j] != x:
        j += 1
        #print (f"  no match on list2[{j}] = {x}")
      #print (f"  check if list2[{j}] == {x}")
      while list2[j] == x:
        #print (f"list1[{i}]: {list1[i]}  list2[{j}]: {list2[j]}")
        match_count += 1
        j += 1
      #print (f"  done finding matches in list2 at j: {j}")
    if match_count > 0:
        print (f"i: {i}  got {match_count} matches in list2.  score: {x*match_count}")
        total += x * match_count
        j = last_j

  return(total)
  

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [line.strip().split() for line in fileinput.input()]

    before = time.time()
    result = part1(lines)
    after = time.time()
    print("results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

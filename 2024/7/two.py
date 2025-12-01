#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

def pipe(a, b):
  val = int(str(a) + str(b))
#  print(f"{a} || {b} = {val}")
  return val

def recurse(target, total, elems):

#  print(" "*(10-len(elems)) + f"recurse({target}, {total}, {elems})")

  if (len(elems) == 1):
    val = total + elems[0]
    if val == target:
#      print(" "*(10-len(elems)) + f"Found a final match for {target} using +");
      return(['+'])

    val = total * elems[0]
    if val == target:
#      print(" "*(10-len(elems)) + f"Found a final match for {target} using *");
      return(['*'])

    val = pipe(total, elems[0])
    if val == target:
#      print(" "*(10-len(elems)) + f"Found a final match for {target} using |");
      return(['||'])

    else:
#      print(" "*(10-len(elems)) + f"No match found for {total} by this path");
      return(None)

  else:
    operators = recurse(target, total+elems[0], elems[1:])
    if operators != None:
#      print(" "*(10-len(elems)) + f"Found a reursive match for {target} prepend + for {elems[0]}");
      return ['+'] + operators

    operators = recurse(target, total*elems[0], elems[1:])
    if operators != None:
#      print(" "*(10-len(elems)) + f"Found a reursive match for {target} prepend * for {elems[0]}");
      return ['*'] + operators

    operators = recurse(target, pipe(total, elems[0]), elems[1:])
    if operators != None:
#      print(" "*(10-len(elems)) + f"Found a reursive match for {target} prepend | for {elems[0]}");
      return ['||'] + operators

def part2(data):
  result = 0

  for target,elems in data.items():
    operators = recurse(target, elems[0], elems[1:])
    if operators is not None:
      result += target
      print(f"Success for {target}: {elems} : {operators} : result: {result}")

  return(result)

if __name__ == '__main__':

  data = {}
  logging.basicConfig(level=logging.INFO)

  lines = [line.replace(':','').strip().split() for line in fileinput.input()]
  for l in lines:
    data[int(l[0])] = [int(i) for i in l[1:]]

#  before = time.time()
#  result = part1(data)
#  after = time.time()
#  print("results: {} ({:.3f} sec)".format(result, (after - before)))

  before = time.time()
  result = part2(data)
  after = time.time()
  print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

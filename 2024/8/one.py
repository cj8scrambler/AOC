#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

def tuple_add(a, b):
  return (a[0] + b[0], a[1] + b[1])

def tuple_sub(a, b):
  return (a[0] - b[0], a[1] - b[1])

def valid(point, data):
  if (point[0] >= 0) and (point[0] < len(data[0])) and \
     (point[1] >= 0) and (point[1] < len(data)):
    return True
  return False

def add_antinode(point, data):
  if (valid(point, data)):
    data[point[1]][point[0]] = '#'
    return True

  return False

def printmap(data):
  for y,row in enumerate(data):
    for x,val in enumerate(row):
      print(val, end="")
    print("")

def part1(data):
  result = 0

  #find the unique antennas
  ants = set()
  for y,row in enumerate(data):
    for x,val in enumerate(row):
      if val != '.':
        ants.add(val)

  print(f"unique antennas: {ants}")
  antmap = {}
  for a in ants:
    antmap[a] = []
    for y,row in enumerate(data):
      for x,val in enumerate(row):
        if val == a:
          antmap[a].append((x,y))

  for ant,points in antmap.items():
    print(f"find antinodes of {ant}: {points}")
    for each in combinations(points, 2):
      delta = tuple_sub(each[0], each[1])
      a1 = tuple_add(each[0], delta)
      a2 = tuple_sub(each[1], delta)
      print(f"ant: {ant} @ {each}: delta: {delta}  a1: {a1}  a2: {a2}")
      add_antinode(a1, data)
      add_antinode(a2, data)

  # Count antinodes
  for y,row in enumerate(data):
    for x,val in enumerate(row):
      if val == '#':
        result += 1

  printmap(data)

  return(result)

def part2(data):
  result = 0

  #find the unique antennas
  ants = set()
  for y,row in enumerate(data):
    for x,val in enumerate(row):
      if val != '.':
        ants.add(val)

  print(f"unique antennas: {ants}")
  antmap = {}
  for a in ants:
    antmap[a] = []
    for y,row in enumerate(data):
      for x,val in enumerate(row):
        if val == a:
          antmap[a].append((x,y))

  for ant,points in antmap.items():
    print(f"find antinodes of {ant}: {points}")
    for each in combinations(points, 2):
      delta = tuple_sub(each[0], each[1])
      base = each[0]
      result= True
      while result:
        a = tuple_add(base, delta)
        result = add_antinode(a, data)
        if result:
          print(f"ant: {ant} @ {each}: delta: {delta}  antinode: {a}")
          base = a

      base = each[1]
      result= True
      while result:
        a = tuple_sub(base, delta)
        result = add_antinode(a, data)
        if result:
          print(f"ant: {ant} @ {each}: delta: {delta}  antinode: {a}")
          base = a

  # Count antinodes and antennas
  for y,row in enumerate(data):
    for x,val in enumerate(row):
      if val != '.':
        result += 1

  printmap(data)

  return(result)

if __name__ == '__main__':

  data = {}
  logging.basicConfig(level=logging.INFO)

  lines = [list(line.strip()) for line in fileinput.input()]

#  before = time.time()
#  result = part1(lines)
#  after = time.time()
#  print("results: {} ({:.3f} sec)".format(result, (after - before)))

  before = time.time()
  result = part2(lines)
  after = time.time()
  print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

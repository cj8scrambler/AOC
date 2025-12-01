#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
import ast
from itertools import combinations 

def is_neighbor(loc1, loc2):

  if (loc1 == (loc2[0]-1, loc2[1]-1)):
    return True
  if (loc1 == (loc2[0]-1, loc2[1])):
    return True
  if (loc1 == (loc2[0]-1, loc2[1]+1)):
    return True

  if (loc1 == (loc2[0], loc2[1]-1)):
    return True
  if (loc1 == (loc2[0], loc2[1]+1)):
    return True

  if (loc1 == (loc2[0]+1, loc2[1]-1)):
    return True
  if (loc1 == (loc2[0]+1, loc2[1])):
    return True
  if (loc1 == (loc2[0]+1, loc2[1]+1)):
    return True

  return False

def neighbor_num(loc, num_map):
  neighbors = set()
  for number in num_map:
    for l in number:
      if is_neighbor(loc, l):
        neighbors.add(str(number))
  return neighbors

def part2(data):
  result = 0
  logging.debug(data)
  num_map = []
  # Map all the numbers
  for y,row in enumerate(data):
    numloc=[]
    for x,char in enumerate(row):
      if char.isdigit():
        numloc.append((y,x))
        if x == (len(row) - 1):
          num_map.append(numloc)
          numloc=[]
      elif len(numloc):
        num_map.append(numloc)
        numloc=[]
  # Now find the *s
  gears={}
  for y,row in enumerate(data):
    for x,char in enumerate(row):
      if char == '*':
        key = "{},{}".format(y,x)
        ns = neighbor_num((y,x), num_map)
        if (len(ns) == 2):
          logging.debug("Found '*' at {} with 2 neighbors:".format(key))
          product = 1
          for each in ns: 
            num=""
            for loc in ast.literal_eval(each):
              num+=data[loc[0]][loc[1]]
            logging.debug("num: {}".format(num))
            product *= int(num) 
          result += product
          logging.debug("product: {}  result: {}".format(product, result))
  return(result)
  
def has_neighbor(numloc, data):
  valid=False
  serial = ""
  for l in numloc:
    serial += data[l[0]][l[1]]
    if has_neighbor_symbol(l, data):
      valid=True
  if valid:
    return(int(serial))

  return(None)

def is_symbol(char):
  if char.isdigit():
    return False
  if char == '.':
    return False

  return True

def has_neighbor_symbol(loc, data):

  y=loc[0]
  x=loc[1]
  if x > 1 and y > 1 and is_symbol(data[y-1][x-1]):
    return True
  if y > 1 and is_symbol(data[y-1][x]):
    return True
  if y > 1 and x < (len(data[0])-1) and is_symbol(data[y-1][x+1]):
    return True

  if x > 1 and is_symbol(data[y][x-1]):
    return True
  if x < (len(data[0])-1) and is_symbol(data[y][x+1]):
    return True

  if x > 1 and y < (len(data)-1) and is_symbol(data[y+1][x-1]):
    return True
  if y < (len(data)-1) and is_symbol(data[y+1][x]):
    return True
  if y < (len(data)-1) and x < (len(data[0])-1) and is_symbol(data[y+1][x+1]):
    return True

  return False

def part1(data):
  result = 0
  logging.debug(data)
  for y,row in enumerate(data):
    numloc=[]
    for x,char in enumerate(row):
      if char.isdigit():
        numloc.append((y,x))
        if x == (len(row) - 1):
          validated = has_neighbor(numloc, data)
          if validated is not None:
            result += validated
            logging.debug("Got new valid number: {}  sum: {}".format(validated, result))
          else:
            logging.debug("Got invalid number: {}".format(numloc))
          numloc=[]
      elif len(numloc):
        validated = has_neighbor(numloc, data)
        if validated is not None:
          result += validated
          logging.debug("Got new valid number: {}  sum: {}".format(validated, result))
        else:
          logging.debug("Got invalid number: {}".format(numloc))
        numloc=[]
      
  return(result)

if __name__ == '__main__':

  logging.basicConfig(level=logging.DEBUG)
  data = []

  for l in [line.strip() for line in fileinput.input()]:
    data.append([*l])

#  before = time.time()
#  result = part1(data)
#  after = time.time()
#  print("results: {} ({:.3f} sec)".format(result, (after - before)))

  before = time.time()
  result = part2(data)
  after = time.time()
  print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

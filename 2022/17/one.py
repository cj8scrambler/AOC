#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from collections import defaultdict
from itertools import combinations 

sys.setrecursionlimit(10000)


def surface_search(obj, point, bounds, surface, visited):

  (x,y,z) = point
  visited.append(point)
  if (x not in bounds[0]) or (y not in bounds[1]) or (z not in bounds[2]):
    logging.debug(f"[{x},{y},{z}] is a out of bounds")
    return

  if (x in obj) and (y in obj[x]) and (z in obj[x][y]):
    logging.debug(f"[{x},{y},{z}] is a surface")
    surface.append(point)
    return

  logging.debug(f"[{x},{y},{z}] is a air")
  for neighbor in ((x+1, y, z), (x, y+1, z), (x, y, z+1),
                   (x-1, y, z), (x, y-1, z), (x, y, z-1)):
    if neighbor not in visited:
      surface_search(obj, neighbor, bounds, surface, visited)

def mark_surface(obj):

  surface = []
  visited = []
  xmin = min(obj.keys())
  xmax = max(obj.keys())
  ymin=999999
  ymax=0
  zmin=9999999
  zmax=0
  for x in obj.keys():
    for y in obj[x].keys():
        if y > ymax:
          ymax=y
        if y < ymin:
          ymin=y
        for z in obj[x][y].keys():
          if z < zmin:
              zmin=z
          if z > zmax:
              zmax=z
 
  surface_search(obj, (xmin-1, ymin-1, zmin-1),
                 (list(range(xmin-1, xmax+2)), 
                  list(range(ymin-1, ymax+2)),
                  list(range(zmin-1, zmax+2))),
                 surface, visited)
  return visited
   

def fill_voids(obj, surface):

  xmin = min(obj.keys())
  xmax = max(obj.keys())
  ymin=999999
  ymax=0
  zmin=9999999
  zmax=0
  for x in obj.keys():
    for y in obj[x].keys():
        if y > ymax:
          ymax=y
        if y < ymin:
          ymin=y
        for z in obj[x][y].keys():
          if z < zmin:
              zmin=z
          if z > zmax:
              zmax=z

  for x in range(xmin, xmax+1):
    for y in range(ymin, ymax+1):
      for z in range(zmin, zmax+1):
          if (x,y,z) not in surface:
            if (x in obj) and (y in obj[x]) and (z in obj[x][y]):
              logging.debug(f"Found internal solid at [{x}][{y}][{z}]")
            else:
              logging.debug(f"Filled internal void at [{x}][{y}][{z}]")
              obj[x][y][z] = {'surface': 6}
        
def calc_surfaces(obj):
  total = 0
  for x in obj.keys():
    for y in obj[x].keys():
        for z in obj[x][y].keys():
          if ((x-1) in obj) and (y in obj[x-1]) and (z in obj[x-1][y]):
            obj[x][y][z]['surface'] -= 1
          if ((x+1) in obj) and (y in obj[x+1]) and (z in obj[x+1][y]):
            obj[x][y][z]['surface'] -= 1
          if (x in obj) and ((y-1) in obj[x]) and (z in obj[x][y-1]):
            obj[x][y][z]['surface'] -= 1
          if (x in obj) and ((y+1) in obj[x]) and (z in obj[x][y+1]):
            obj[x][y][z]['surface'] -= 1
          if (x in obj) and (y in obj[x]) and ((z-1) in obj[x][y]):
            obj[x][y][z]['surface'] -= 1
          if (x in obj) and (y in obj[x]) and ((z+1) in obj[x][y]):
            obj[x][y][z]['surface'] -= 1
          logging.debug(f"[{x}][{y}][{z}] surface: {obj[x][y][z]['surface']}")
          total += obj[x][y][z]['surface']
  return total

def print_obj(obj):
  xmin = min(obj.keys())
  xmax = max(obj.keys())
  ymin=999999
  ymax=0
  zmin=9999999
  zmax=0
  for x in obj.keys():
    for y in obj[x].keys():
        if y > ymax:
          ymax=y
        if y < ymin:
          ymin=y
        for z in obj[x][y].keys():
          if z < zmin:
              zmin=z
          if z > zmax:
              zmax=z

  for x in range(xmin, xmax+1):
    for y in range(ymin, ymax+1):
      for z in range(zmin, zmax+1):
        if (x in obj) and (y in obj[x]) and (z in obj[x][y]):
          print('#', end='')
        else:
          print('.', end='')
      print('')
    print('')
    print('')
         
def part2(data):
  restult = 0
  obj = defaultdict(lambda: defaultdict(dict))

  for line in lines:
    (x,y,z) = tuple(int(i) for i in line.split(','))
    obj[x][y][z] = {'surface': 6}
    logging.debug(f"Added obj[{x}][{y}][{z}]: {obj[x][y][z]}")

  surface = mark_surface(obj)
  fill_voids(obj, surface)
  return calc_surfaces(obj)


def part1(data):
  restult = 0
  obj = defaultdict(lambda: defaultdict(dict))

  for line in lines:
    (x,y,z) = tuple(int(i) for i in line.split(','))
    obj[x][y][z] = {'surface': 6}
    logging.debug(f"Added obj[{x}][{y}][{z}]: {obj[x][y][z]}")

  print_obj(obj)

  return calc_surfaces(obj)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [line.strip() for line in fileinput.input()]

    before = time.time()
    result = part1(lines)
    after = time.time()
    print("part 1 results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

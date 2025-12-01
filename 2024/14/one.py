#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

WIDTH = 101
HEIGHT = 103
#WIDTH = 11
#HEIGHT = 7

def safety(data):

#  Map into a quadrant:  0 1
#                        2 3
  quad = [0, 0, 0, 0]

  for robot in data.values():
    if robot['pos'][0] < (WIDTH-1)/2:
      if robot['pos'][1] < (HEIGHT-1)/2:
        quad[0] += 1
        #print(f"{robot['pos']} quad-1 now: {quad[0]}")
      elif robot['pos'][1] >= (HEIGHT+1)/2:
        quad[2] += 1
        #print(f"{robot['pos']} quad-3 now: {quad[2]}")
      #else:
        #print(f"{robot['pos']} on left Y line")
    elif robot['pos'][0] >= (WIDTH+1)/2:
      if robot['pos'][1] < (HEIGHT-1)/2:
        quad[1] += 1
        #print(f"{robot['pos']} quad-2 now: {quad[1]}")
      elif robot['pos'][1] >= (HEIGHT+1)/2:
        quad[3] += 1
        #print(f"{robot['pos']} quad-4 now: {quad[3]}")
      #else:
        #print(f"{robot['pos']} on right Y line")
    #else:
      #print(f"{robot['pos']} on X line")
 
  result = 1
  for q in quad:
    result *= q
  #print(f"Safety factor {quad}: {result}")
  return(result)

def valid(point, data):
  if (point[0] >= 0) and (point[0] < len(data[0])) and \
     (point[1] >= 0) and (point[1] < len(data)):
    return True
  return False

widest=0
def printmap(data, quads):
  global widest
  doprint = 0
  mapdata = [['.' for x in range(WIDTH)] for y in range(HEIGHT)]

  for robot in data.values():
    (x, y) =(robot['pos'][0], robot['pos'][1])
    if mapdata[y][x] == '.':
      mapdata[y][x] = 1
    else:
      mapdata[y][x] += 1

#  # see if it's a size new record
#  for y,row in enumerate(mapdata):
#    if (WIDTH - row.count('.') > widest):
#      widest = WIDTH - row.count('.')
#      doprint = True
#      print(f"New record width: {widest}")

#  # see if it's symetric
#  for y,row in enumerate(mapdata):
#    middle = int((WIDTH+1)/2)
#    if (row[0:middle-1] == list(reversed(row[middle:None]))):
#      if (WIDTH != row.count('.')):
#        doprint += 1

  # see if it's connected'ish
  for y,row in enumerate(mapdata):
    for x,val in enumerate(row):
      if (val != '.') and (valid((x-1,y+1), mapdata) and mapdata[y+1][x-1] != '.'):
        doprint += 1
      if (val != '.') and (valid((x+1,y+1), mapdata) and mapdata[y+1][x+1] != '.'):
        doprint += 1

  if doprint > 200:
    for y,row in enumerate(mapdata):
      for x,val in enumerate(row):
        if quads and ((x == (WIDTH-1)/2) or ((y == (HEIGHT-1)/2))):
          print(' ', end="")
        else:
          print(val, end="")
      print("")
    return doprint
  return False

def point_add(a, b):
  new_x = (a[0] + b[0])
  if new_x < 0:
    new_x += WIDTH
  else:
    new_x %= WIDTH

  new_y = (a[1] + b[1])
  if new_y < 0:
    new_y += HEIGHT
  else:
    new_y %= HEIGHT

  return(new_x, new_y)

def move(robots):
  for i,robot in robots.items():
    new = point_add(robot['pos'], robot['vel'])
    #print(f"robot-{i}: start: {robot['pos']}  vel: {robot['vel']}  -> {new}")
    robot['pos'] = new

def part2(data):
  return(0)
  
def part1(data):
  result = 0

  robots = defaultdict(dict)
  for i,line in enumerate(data):
    (pos_data, vel_data) = line.split()
    pos = tuple([int(i) for i in pos_data.split('=')[1].split(',')])
    vel = tuple([int(i) for i in vel_data.split('=')[1].split(',')])
    robots[i] = {'pos': pos, 'vel': vel}


  printmap(robots, False)
  for s in range(100000):
    s += 1
    move(robots)
    r = printmap(robots, False)
    if r:
      print(f"Found {r} symetric rows at {s} seconds")

 # printmap(robots, True)
  return(safety(robots))

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [line.strip() for line in fileinput.input()]

    before = time.time()
    result = part1(lines)
    after = time.time()
    print("results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

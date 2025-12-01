#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 

W_MIN=99999
W_MAX=0
WIDTH=0 
HEIGHT=0 

def print_map(image):
  for y in range(HEIGHT):
    for x in range(WIDTH):
      print(image[y][x], end='')
    print("")

def drop_sand(rocks, loc):
  global W_MIN

  sx,sy = (loc)
 
  if (sx <= 0) or (sx >= WIDTH) or (sy >= (HEIGHT - 1)):
    logging.debug(f"  Sand falls forever at ({sx},{sy})")
    return False
  #try down
  if rocks[sy+1][sx] == '.':
    logging.debug(f"  Sand moving down to: ({sx}, {sy+1})")
    return drop_sand(rocks,(sx, sy+1))

  #try down-left
  elif rocks[sy+1][sx-1] == '.':
    logging.debug(f"  Sand moving down-left to: ({sx-1}, {sy+1})")
    return drop_sand(rocks,(sx-1, sy+1))

  #try down-right
  elif rocks[sy+1][sx+1] == '.':
    logging.debug(f"  Sand moving down-right to: ({sx+1}, {sy+1})")
    return drop_sand(rocks,(sx+1, sy+1))

  rocks[sy][sx] = 'o'
  if (sx, sy) == (500-W_MIN, 0):
    logging.debug(f"  Sand is full")
    return False
  else:
    logging.debug(f"  Sand settled at ({sx+W_MIN},{sy})")
    return True
  

def part2(data):

  global W_MIN
  global W_MAX
  global HEIGHT
  global WIDTH

  result=0
  points = []
  for row,line in enumerate(data):
    points.append([])
    for point in line.replace('-', '').replace('>', '').replace('(','').replace(')','').split():
      (x, y) = tuple(int(p) for p in point.split(','))
      points[-1].append((x,y))
      if x > W_MAX:
        W_MAX=x
      if x < W_MIN:
        W_MIN=x
      if y > HEIGHT:
        HEIGHT=y
    
  HEIGHT += 3
  realwidth = W_MAX - W_MIN
  print(f"  width: max({HEIGHT}, {WIDTH+3}")
  WIDTH = max(3*HEIGHT, WIDTH+3)
  W_MIN -= int((WIDTH - realwidth) / 2)
  print(f"Overall: {WIDTH} x {HEIGHT} (subtract {W_MIN})")

  rocks = [['.' for x in range(WIDTH)] for y in range(HEIGHT)]

  for segment in points:
    prev = None
    for (x,y) in segment: 
      print(f"{prev} -> {x},{y}")
      rocks[y][x-W_MIN] = '#'
      if prev:
        if prev[0] == x:
          for i in range(min(prev[1],y)+1, max(prev[1],y)):
            rocks[i][x-W_MIN] = '#'
        elif prev[1] == y:
          for i in range(min(prev[0],x)+1, max(prev[0],x)):
            rocks[y][i-W_MIN] = '#'
        else:
          raise Exception("not a straight line")
      
      prev = (x,y)

  #draw floor
  for i in range(WIDTH):
    rocks[-1][i] = '-'

  print_map(rocks)

  grains = 1
  while (drop_sand(rocks, (500-W_MIN, 0))):
    grains += 1
    logging.debug(f"drop sand grain {grains}")

  print_map(rocks)

  return(grains) 
  
def part1(data):

  global W_MIN
  global W_MAX
  global HEIGHT
  global WIDTH

  result=0
  points = []
  for row,line in enumerate(data):
    points.append([])
    for point in line.replace('-', '').replace('>', '').replace('(','').replace(')','').split():
      (x, y) = tuple(int(p) for p in point.split(','))
      points[-1].append((x,y))
      if x > W_MAX:
        W_MAX=x
      if x < W_MIN:
        W_MIN=x
      if y > HEIGHT:
        HEIGHT=y
    
  WIDTH = W_MAX - W_MIN +3
  HEIGHT += 2
  W_MIN -= 1
  print(f"Overall: {WIDTH} x {HEIGHT} (subtract {W_MIN})")

  rocks = [['.' for x in range(WIDTH)] for y in range(HEIGHT)]

  for segment in points:
    prev = None
    for (x,y) in segment: 
      print(f"{prev} -> {x},{y}")
      rocks[y][x-W_MIN] = '#'
      if prev:
        if prev[0] == x:
          for i in range(min(prev[1],y)+1, max(prev[1],y)):
            rocks[i][x-W_MIN] = '#'
        elif prev[1] == y:
          for i in range(min(prev[0],x)+1, max(prev[0],x)):
            rocks[y][i-W_MIN] = '#'
        else:
          raise Exception("not a straight line")
      
      prev = (x,y)

  grains = 0
  while (drop_sand(rocks, (500-W_MIN, 0))):
    grains += 1
    logging.debug(f"drop sand grain {grains}")

  print_map(rocks)

  return(grains) 

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [line.strip() for line in fileinput.input()]

#    before = time.time()
#    result = part1(lines)
#    after = time.time()
#    print("results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

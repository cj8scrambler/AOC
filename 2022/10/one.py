#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 

WIDTH=40
HEIGHT=6 

def print_image(image):
  for y in range(HEIGHT):
    for x in range(WIDTH):
      print(image[y][x], end='')
    print("")

def part2(data):

  cycle=-1
  ticks=0
  reg=1
  result=0
  image = [['?' for x in range(WIDTH)] for y in range(HEIGHT)]

  for line in data:
    cmd = line.split()
    if cmd[0] == "noop":
      ticks = 1
    elif cmd[0] == 'addx':
      ticks = 2
    for t in range(ticks):
      cycle += 1
      x = cycle % WIDTH
      y = cycle // WIDTH
      draw='.'
      if (x >= reg-1) and (x <= reg+1):
        draw='#'
      logging.debug("cycle-{}: [{}] ticks={} X={} [{},{}]: {}".format(cycle, line, ticks, reg, y, x, draw))
      image[y][x]=draw
      logging.debug("  line {}: {}".format(y, image[y]))
      
    if cmd[0] == "noop":
      pass
    elif cmd[0] == 'addx':
      reg += int(cmd[1])

  if cycle < (HEIGHT * WIDTH):
    for t in range(cycle, (HEIGHT*WIDTH)):
      cycle += 1
      logging.debug("cycle-{}: [{}] ticks={} X={} [{},{}]: {}".format(cycle, line, ticks, reg, x, y, draw))

  print_image(image)

  return(0)
  
def part1(data, cycles):

  cycle=0
  ticks=0
  x=1
  result=0

  for line in data:
    cmd = line.split()
    if cmd[0] == "noop":
      ticks = 1
    elif cmd[0] == 'addx':
      ticks = 2
    for t in range(ticks):
      cycle += 1
      if cycle in cycles:
        result += cycle * x
        logging.info("cycle-{}: [{}] ticks={} X={} result={}".format(cycle, line, ticks, x, result))
      else:
        logging.debug("cycle-{}: [{}] ticks={} X={}".format(cycle, line, ticks, x))
      
    if cmd[0] == "noop":
      pass
    elif cmd[0] == 'addx':
      x += int(cmd[1])

  if cycle < cycles[-1]:
    for t in range(cycle, cycles[-1]):
      cycle += 1
      logging.debug("cycle-{}: [{}] ticks={} X={}".format(cycle, line, ticks, x))

  return(result)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [line.strip() for line in fileinput.input()]

#    before = time.time()
#    result = part1(lines, [20, 60, 100, 140, 180, 220, 250])
#    after = time.time()
#    print("results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

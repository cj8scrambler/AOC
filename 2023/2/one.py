#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 

def part2(data):
  logging.debug(data)
  result = 0
  for gamenum,gamedata in data.items():
    minred = mingreen = minblue = 0
    for rnd in gamedata:
      for each in rnd:
        if each[0] > minred:
          minred = each[0]
        if each[1] > mingreen:
          mingreen = each[1]
        if each[2] > minblue:
          minblue = each[2]
    logging.debug("Game-{} min is: {}  power: {}".format(gamenum, (minred, mingreen, minblue), minred*mingreen*minblue))
    result += minred * mingreen * minblue
  return(result)
  
def part1(data, target):
  logging.debug(data)
  result = 0
  for gamenum,gamedata in data.items():
    valid = True
    for rnd in gamedata:
      for each in rnd:
        if each[0] > target[0] or each[1] > target[1] or each[2] > target[2]:
          valid = False
          logging.debug("Game-{} is not possible".format(gamenum))
          break;
    if valid:
      result += int(gamenum)
      logging.debug("Game-{} IS possible: new result: {}".format(gamenum, result))
  return(result)

if __name__ == '__main__':

  logging.basicConfig(level=logging.DEBUG)

  lines = [line.strip() for line in fileinput.input()]

  data = {}
  for l in lines:
    g,c = l.split(':', 1)    
    s,game = g.split()
    data[game] = []
    for rndnum,rnddata in enumerate(c.split(';')):
      data[game].append([])
      red = green = blue = 0
      for info in rnddata.split(','):
        num,color = info.lstrip().split(' ')
        if color == 'red':
          red = int(num)
        elif color == 'green':
          green = int(num)
        elif color == 'blue':
          blue = int(num)
        else:
          raise Exception("Unkown color: {}".format(color))
      data[game][int(rndnum)].append((red,green,blue))

#  before = time.time()
#  result = part1(data, (12, 13, 14))
#  after = time.time()
#  print("results: {} ({:.3f} sec)".format(result, (after - before)))

  before = time.time()
  result = part2(data)
  after = time.time()
  print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

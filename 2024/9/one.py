#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 
from collections import defaultdict 

def checksum(disk):
  checksum = 0
  for i,val in enumerate(disk):
    checksum += i*val
  return checksum
    
  
def compact(disk):

  blank = 0
  last = len(disk) - 1

  while '.' in disk:
    while disk[blank] != '.':
      blank += 1
    while disk[last] == '.':
      last -=1
      last -=1
    disk[blank] = disk.pop(last)
    while disk[-1] == '.':
      disk.pop()
    last = len(disk) - 1
    #printdisk(disk)

def printdisk(disk):
  for val in disk:
    print(val, end="")
  print("")

def part2(data):
  return(0)
  
def part1(data):

  state = 0
  fileid = 0
  disk = []

  for val in data:
    if (state % 2 == 0):
      disk += [fileid]*val
      fileid += 1
    else:
      disk += ['.']*val
    state += 1

  printdisk(disk)

  compact(disk)

  return checksum(disk)
    
if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [list(line.strip()) for line in fileinput.input()]

    before = time.time()
    result = part1([int(i) for i in lines[0]])
    after = time.time()
    print("results: {} ({:.3f} sec)".format(result, (after - before)))

#    before = time.time()
#    result = part2(lines)
#    after = time.time()
#    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

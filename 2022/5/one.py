#!/usr/bin/python

import logging
import sys
import re
import fileinput
import time
from itertools import combinations 

MAX_STACKS=9

def part1(data):

  stacks = [[] for _ in range(MAX_STACKS)]
  for line in data:
    if '[' in line:
      if ((len(line) >= 2) and line[1] != ' '):
        stacks[0].insert(0, line[1])
      if ((len(line) >= 6) and line[5] != ' '):
        stacks[1].insert(0, line[5])
      if ((len(line) >= 10) and line[9] != ' '):
        stacks[2].insert(0, line[9])
      if ((len(line) >= 14) and line[13] != ' '):
        stacks[3].insert(0, line[13])
      if ((len(line) >= 18) and line[17] != ' '):
        stacks[4].insert(0, line[17])
      if ((len(line) >= 22) and line[21] != ' '):
        stacks[5].insert(0, line[21])
      if ((len(line) >= 26) and line[25] != ' '):
        stacks[6].insert(0, line[25])
      if ((len(line) >= 30) and line[29] != ' '):
        stacks[7].insert(0, line[29])
      if ((len(line) >= 34) and line[33] != ' '):
        stacks[8].insert(0, line[33])
    if 'move' in line:
      g = re.match( r"move ([0-9]+) from ([0-9]+) to ([0-9]+)", line)
      if g:
        moves = int(g.group(1))
        source = int(g.group(2)) - 1
        dest = int(g.group(3)) - 1

        for m in range(moves):
            print(" move #{} from {} to {}".format(m+1, source, dest))
            stacks[dest].append(stacks[source].pop())

  result = ''
  for s in stacks:
    if s:
      result += s.pop()
    
  return(result)

def part2(data):

  stacks = [[] for _ in range(MAX_STACKS)]
  for line in data:
    if '[' in line:
      if ((len(line) >= 2) and line[1] != ' '):
        stacks[0].insert(0, line[1])
      if ((len(line) >= 6) and line[5] != ' '):
        stacks[1].insert(0, line[5])
      if ((len(line) >= 10) and line[9] != ' '):
        stacks[2].insert(0, line[9])
      if ((len(line) >= 14) and line[13] != ' '):
        stacks[3].insert(0, line[13])
      if ((len(line) >= 18) and line[17] != ' '):
        stacks[4].insert(0, line[17])
      if ((len(line) >= 22) and line[21] != ' '):
        stacks[5].insert(0, line[21])
      if ((len(line) >= 26) and line[25] != ' '):
        stacks[6].insert(0, line[25])
      if ((len(line) >= 30) and line[29] != ' '):
        stacks[7].insert(0, line[29])
      if ((len(line) >= 34) and line[33] != ' '):
        stacks[8].insert(0, line[33])
    if 'move' in line:
      g = re.match( r"move ([0-9]+) from ([0-9]+) to ([0-9]+)", line)
      if g:
        moves = int(g.group(1))
        source = int(g.group(2)) - 1
        dest = int(g.group(3)) - 1

        temp = []
        print(" move {} ({}) from {} to {}".format(moves, stacks[source][-moves:],source, dest))
        for m in range(moves):
            temp.append(stacks[source].pop())
        for m in range(moves):
            stacks[dest].append(temp.pop())
        print(stacks)

  result = ''
  for s in stacks:
    if s:
      result += s.pop()
  return result
    
if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    lines = [line for line in fileinput.input()]

    before = time.time()
    result = part1(lines)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

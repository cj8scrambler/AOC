#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 


def part2(data):

  result=0

  return(grains) 

def go(valves, loc, pressure, mins, visited):

  children = []
  visited.append(loc)

  logging.debug(f"{' '*(30-mins)}Visiting {loc} (visited: {visited})")
  mins -= 1 # walking time
  if mins == 0:
    logging.debug(f"{' '*(30-mins)}Hit 0 time walking to {loc}")
    return pressure

  newpath = False
  for t in valves[loc]['to']:
    if t not in visited:
      children.append(go(valves, t, pressure, mins, visited))
      newpath = True

  mins -= 1 # turn on valve
  if mins == 0:
    logging.debug(f"{' '*(30-mins)}Hit 0 mins turning on valve {loc}; returning best: {max([pressure]+children)}")
    return max([pressure]+children)

  pressure += valves[loc]['rate'] * mins
  logging.debug(f"{' '*(30-mins)}Valve-{loc} mins: {mins}  contributing {valves[loc]['rate'] * mins} pressure, now: {pressure}")

  if not newpath:
    logging.debug(f"{' '*(30-mins)}Valve-{loc} mins: {mins}  I've been everywhere")
    return pressure

  for t in valves[loc]['to']:
    if t not in visited:
      children.append(go(valves, t, pressure, mins, visited))

  logging.debug(f"{' '*(30-mins)}Exhausted all paths from Valve-{loc} best: {max([pressure]+children)}")
  return (max([pressure]+children))
  
def part1(data):

  valves = {}

  exp = 'Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? (.+)?'
  for row,line in enumerate(data):
    m = re.match(exp, line)
    if m:
      logging.debug(f"Match: {m.groups()}")
    else:
      logging.debug(f"No Match: {line}")
    if m.group(1) not in valves:
      valves[m.group(1)] = {'rate': int(m.group(2)), 'to': []}
      for to in m.group(3).split(','):
        valves[m.group(1)]['to'].append(to.strip())

  print(valves)
  return go(valves, 'AA', 0, 30, [])
    

  return(0) 

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    lines = [line.strip() for line in fileinput.input()]

    before = time.time()
    result = part1(lines)
    after = time.time()
    print("results: {} ({:.3f} sec)".format(result, (after - before)))

#    before = time.time()
#    result = part2(lines)
#    after = time.time()
#    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

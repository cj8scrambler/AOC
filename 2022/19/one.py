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


def part2(data):
  restult = 0
  return result


def part1(data):
  result = 0
  blueprints = {}
  exp = 'Blueprint ([0-9]+): Each ore robot costs ([0-9]+) ore. Each clay robot costs ([0-9]+) ore. Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay. Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian.'
  rorder = ['ore', 'clay', 'obsidian', 'geode']

  for row,line in enumerate(data):
    m = re.match(exp, line)
    if m:
      blueprints[int(m.group(1))] = {'ore': [('ore', int(m.group(2)))],
                                    'clay': [('ore', int(m.group(3)))],
                                    'obsidian': [('ore', int(m.group(4))), ('clay', int(m.group(5)))],
                                    'geode': [('ore', int(m.group(6))), ('obsidian', int(m.group(7)))]}
    else:
      logging.debug(f"No Match: {line}")
      raise("Parse Error")

  logging.debug(f"blueprints: {blueprints}")
  for bid,b in blueprints.items():
    robots = {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}
    material = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}
    time = 0
    while time < 24:
      time += 1
      newbots = []
      for rtype in b.keys():
        make_robot = True
        for mreq in b[rtype]:
          if material[mreq[0]] < mreq[1]:
            logging.debug(f"  Not enough {mreq[0]} to make a {rtype}")
            make_robot = False
        if make_robot:
          logging.debug(f"  Found enough {mreq[0]} to make a {rtype}")
          newbots.append(rtype)
          
      for rtype,rnum in robots.items():
        logging.debug(f"  Roboot {rtype} adds {rnum} (was {material[rtype]})")
        material[rtype] += rnum

      for rtype in newbots:
        logging.debug(f"  Create a new {rtype} robot")
        for (mtype,mamount) in b[rtype]:
          logging.debug(f"    use {mamount} x {mtype}")
          material[mtype] -= mamount
        robots[rtype] += 1

      logging.debug(f"Time: {time}  Robots: ore: {robots['ore']}  clay: {robots['clay']}  obsidian: {robots['obsidian']}  geode: {robots['geode']}")
      logging.debug(f"Time: {time}  Resources: ore: {material['ore']}  clay: {material['clay']}  obsidian: {material['obsidian']}  geode: {material['geode']}")
  

  return result

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    lines = [line.strip() for line in fileinput.input()]

    before = time.time()
    result = part1(lines)
    after = time.time()
    print("part 1 results: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

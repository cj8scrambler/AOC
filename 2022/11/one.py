#!/usr/bin/python3

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 

def part2(data):
  pass

class Monkey:
  _items = []

  def __init(self, items, op, op_arg, test, test_arg):
    self.__items = items
    self.__items = items
    if op == 'times':
      self._op = self.mul
    if op == 'plus':
      self._op = self.add
    logging.debug("New Monkey")

  def mul(self):
    if type(self._op_arg) is int:
      return self._op_arg * self._old
    else :
      return self._old * self._old

  def add(self):
    if type(self._op_arg) is int:
      return self._op_arg * self._old
    else:
      return self._old * self._old

  def add_items(self, items):
    for i in items:
      self._items.append(int(i))
    logging.debug("  Added Items")

  def set_operation

monkeys = [
  Monkey([79,98], times, 19, divide, 23)

def part1(data):

  result = 0

  monkeys = []

  for line in data:
    logging.debug("Line: {}".format(line))
    if "Monkey " in line:
      monkeys.append(Monkey())
    elif "Starting items:" in line:
      monkeys[-1].add_items(line.split(':')[1].split(','))
    elif "Operation:" in line:
      
      monkeys[-1].set_oper(
    else:
      logging.debug(" No Match")

  print(monkeys)
  return(result)

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

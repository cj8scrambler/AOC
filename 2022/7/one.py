#!/usr/bin/python

import logging
import sys
import re
import os
import fileinput
import time
from itertools import combinations 

class File:
  def __init__(self, name, size, directory):
    self._name = name
    self._size = size
    self._parent = directory
    logging.debug("Created file '{}' ({})".format(self.__str__(), self._size))

  def __str__(self):
    return self._parent.__str__() + '/' + self._name

  def name(self):
    return self._name

  def size(self):
    return self._size
    
class Dir:
  def __init__(self, name, parent=None):
    self._name = name
    self._parent = parent
    self._subdirs = []
    self._files = []

  def __str__(self):
    if self._name == '/':
      return ''
    return self.parent().__str__() + '/' + self._name

  def name(self):
    return self._name

  def parent(self):
    return self._parent

  def cd(self, name):
    for d in self._subdirs:
      if name == d.name():
        return d
    logging.error("No such directory:  {}/{}".format(self,name))
    raise Exception

  def mkdir(self, name):
    for d in self._subdirs:
      if name == d.name():
        logging.debug("  Directory '{}' already exists".format(d))
        return d
    self._subdirs.append(Dir(name=name, parent=self))
    return self._subdirs[-1]

  def mkfile(self, name, size):
    for f in self._files:
      if name == f.name():
        logging.debug("  File '{}' already exists".format(f))
        return f
    self._files.append(File(name=name, size=size, directory=self))
    return self._files[-1]

  def print_tree(self, space=''):
    print("{} {}/".format(space, self.name()))
    for d in self._subdirs:
      d.print_tree(space=space+'  ')
    for f in self._files:
      print("{}   {} ({})".format(space, f.name(), f.size()))

  def size(self):
    size = 0
    for d in self._subdirs:
      size += d.size()
    for f in self._files:
      size += f.size()
    return size

  def subdirs(self):
    """ return a [Dir] of all subdirectories recursively """
    subdirs = []
    for d in self._subdirs:
      subdirs += d.subdirs()
    subdirs.append(self)
    return subdirs

def part1(data):

  root = Dir('/')
  pwd = None;

  for l in data:
    cmd = l.split()
    logging.debug("cmd: {}".format(cmd))
    if (cmd[0] == '$'):
      if (cmd[1] == 'cd'):
        if cmd[2] == '/':
          pwd = root
          logging.debug('  set pwd = {}'.format(pwd.name()))
        elif cmd[2] == '..':
          pwd = pwd.parent()
          logging.debug('  set pwd = {}'.format(pwd.name()))
        else:
          #pwd = pwd.mkdir(cmd[2])
          pwd = pwd.cd(cmd[2])
      elif (cmd[1] == 'ls'):
          logging.debug('  ignore ls command'.format(pwd))
      else:
          logging.error('Unkown command: {}'.format(cmd[2]))
          raise Exception
    else:
      if cmd[0] == 'dir':
        newdir = pwd.mkdir(cmd[1])
        logging.debug('  created {}'.format(newdir))
      else:  
        pwd.mkfile(cmd[1], int(cmd[0]))

  root.print_tree()

  total = 0
  for d in root.subdirs():
    s = d.size()
    if s <= 100000:
      total+= s
      logging.debug("{} adds {}: {}".format(d, s, total))
  print("")
  print("### Part 1: {}".format(total))
  print("")

  disk = 70000000
  avail = disk - root.size()
  need = 30000000
  target_free = need-avail
  logging.debug("Available: {}  Need to free: {}".format(avail, target_free))

  best = (root, root.size())
  for d in root.subdirs():
    s = d.size()
    if s >= target_free:
      if s < best[1]:
        best = (d, s)
        logging.debug("{} is best new target: {}".format(d, s))
      else:
        logging.debug("{} is big enough but not as good: {}".format(d, s))
    else:
      logging.debug("{} is not big enough to help: {}".format(d, s))
  logging.debug("Best directory to remove: {}  ({})".format(best[0], best[1]))

  print("### Part 2: {}".format(best[1]))
  print("")

  


  return(total)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [line for line in fileinput.input()]

    before = time.time()
    result = part1(lines)
    after = time.time()
    print("part 1 result: {} ({:.3f} sec)".format(result, (after - before)))

#    before = time.time()
#    result = part2(lines[0])
#    after = time.time()
#    print("part 2 result: {} ({:.3f} sec)".format(result, (after - before)))

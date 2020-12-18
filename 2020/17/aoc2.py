#!/usr/bin/python3

import logging
import sys
import fileinput
import time
import re
import copy
from itertools import combinations 
  

def show(data):
    #logging.debug("show: {}".format(data))
    for w in range(len(data)):
        for z in range(len(data[w])):
            logging.error ("w=%d z=%d" % (w,z))
            for y in data[w][z]:
                line = ""
                for x in y:
                    line = line + x
                logging.error ("{}".format(line))

def grow(data):
    #logging.debug("grow: {}".format(data))
    newzw = len(data) + 2
    newxy = len(data[0][0]) + 2
    logging.debug("grow: nezw: %d nexy: %d" % (newzw, newxy))
    for w in data:
        for z in w:
            for y in z:
                y.insert(0,'.')
                y.append('.')
            z.insert(0, ['.'] * newxy)
            z.append(['.'] * newxy)
        w.insert(0, [['.'] * newxy for i in range(newxy)])
        w.append([['.'] * newxy for i in range(newxy)])
    
    data.insert(0, [[['.'] * newxy for i in range(newxy)] for j in range(newzw)])
    data.append([[['.'] * newxy for i in range(newxy)] for j in range(newzw)])

    logging.debug("newdata: {}".format(data))

def neighbors(data, x, y, z, w):

    n=0
    logging.debug("  Find neighbors of: [%d, %d, %d, %d]" % (w, z, y, x))
    for wr in range(w-1,w+2):
        if (wr < 0) or (wr >= len(data)):
            #logging.debug("Skip invalid w: %d" % (zr))
            continue
        for zr in range(z-1,z+2):
            if (zr < 0) or (zr >= len(data[0])):
                #logging.debug("Skip invalid z: %d" % (zr))
                continue
            for yr in range(y-1,y+2):
                if (yr < 0) or (yr >= len(data[0][0])):
                    #logging.debug("Skip invalid y: %d" % (yr))
                    continue
                for xr in range(x-1,x+2):
                    if (xr < 0) or (xr >= len(data[0][0])):
                        #logging.debug("Skip invalid x: %d" % (xr))
                        continue
                    if (wr == w) and (xr == x) and (yr == y) and (zr == z):
                        #logging.debug("  skip me: [%d, %d, %d, %d]" % (wr, zr, yr, xr))
                        continue
                    if (data[wr][zr][yr][xr] == '#'):
                        logging.debug("    found neighbor: [%d, %d, %d, %d]" % (wr, zr, yr, xr))
                        n += 1

    logging.debug("  [%d, %d, %d, %d] has %d neighbors" % (w, z, y, x, n))
    return n

def cycle(data):

    logging.debug("Cycle")
    newdata = copy.deepcopy(data)
    logging.debug("  w range: {}".format(range(0, len(data))))
    for w in range(0, len(data)):
      logging.debug("  z range: {}".format(range(0, len(data[w]))))
      for z in range(0, len(data[w])):
          logging.debug("  y range: {}".format(range(0, len(data[w][z]))))
          for y in range(0, len(data[w][z])):
              logging.debug("  x range: {}".format(range(0, len(data[w][z]))))
              for x in range(0, len(data[w][z])):
                  logging.debug("Cycle: on [%d,%d,%d,%d]" % (w,z, y, x))
                  n = neighbors(data, x, y, z, w)
                  if data[w][z][y][x] == '#':
                      if (n != 2) and (n != 3):
                          newdata[w][z][y][x] = '.'
                          logging.info("  [%d,%d,%d,%d] # -> %c" % (w, z, y, x, newdata[w][z][y][x]))
                  else:
                      if (n == 3):
                          newdata[w][z][y][x] = '#'
                          logging.info("  [%d,%d,%d,%d] . -> %c" % (w, z, y, x, newdata[w][z][y][x]))
    return newdata

def count(data):

    sum = 0

    logging.debug("  w range: {}".format(range(0, len(data))))
    for w in range(0, len(data)):
      logging.debug("  z range: {}".format(range(0, len(data[w]))))
      for z in range(0, len(data[w])):
          logging.debug("  y range: {}".format(range(0, len(data[z]))))
          for y in range(0, len(data[w][z])):
              logging.debug("  x range: {}".format(range(0, len(data[z]))))
              for x in range(0, len(data[w][z])):
                  if data[w][z][y][x] == '#':
                      sum += 1
    return sum


def part2(data):

    #show(data)
    for each in range(6):
        logging.error("##### Cycle %d ######" % (each +1))
        grow(data)
        newdata = cycle(data)
        #show(newdata)
        data = newdata
        logging.debug("")
    return count(data)


if __name__ == '__main__':

    logging.basicConfig(level=logging.ERROR)

    data = [[[]]]

    for line in fileinput.input():
        data[0][0].append(list(line.rstrip()))

    result = part2(data)
    print("Part 2: %d" % result)

    #result = part2(rules, [tickets[0]] + goodlist)
    #print("Part 2: {}".format(result))

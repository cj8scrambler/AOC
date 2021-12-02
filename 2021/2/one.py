#!/usr/bin/python

import logging
import sys
import fileinput
import time
  
def part1(lines):
    p = 0
    d = 0
    for [move,dis] in lines:
        if move == "forward":
            p += int(dis)
        if move == "down":
            d += int(dis)
        if move == "up":
            d -= int(dis)
        logging.debug("{}:{}  => p={} d={}".format(move,dis,p,d))

    logging.debug("final p={} d={}".format(p, d))
    return(p*d)

def part2(lines):
    p = 0
    a = 0
    d = 0
    for [move,dis] in lines:
        if move == "forward":
            p += int(dis)
            d += a * int(dis)
        if move == "down":
            a += int(dis)
        if move == "up":
            a -= int(dis)
        logging.debug("{}:{}  => p={} a={} d={}".format(move,dis,p,a,d))
    logging.debug("final p={} d={}".format(p, d))
    return(p*d)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    lines = [line.split() for line in fileinput.input()]

    before = time.time()
    result = part1(lines)
    after = time.time()
    print("part 1 product: {} ({:.3f} sec)".format(result, (after - before)))

    before = time.time()
    result = part2(lines)
    after = time.time()
    print("part 2 product: {} ({:.3f} sec)".format(result, (after - before)))
